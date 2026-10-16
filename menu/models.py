from django.db import models
from django.core.validators import FileExtensionValidator
import qrcode
from io import BytesIO
from django.core.files import File

class RestaurantSettings(models.Model):
    name = models.CharField(max_length=150, default="Sky Bliss — The AeroPub")
    tagline = models.CharField(max_length=255, default="Rooftop Lounge & Dining Experience • Pondicherry")
    permanent_qr_image = models.ImageField(upload_to='restaurant_qr/', blank=True, null=True)
    menu_pdf = models.FileField(
        upload_to='menu_pdfs/',
        blank=True,
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=['pdf'])],
        help_text="Upload official restaurant PDF menu here"
    )
    pdf_updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Restaurant Settings & Permanent QR"
        verbose_name_plural = "Restaurant Settings & Permanent QR"

    def __str__(self):
        return self.name

    def generate_permanent_qr(self, domain=""):
        url = f"{domain.rstrip('/')}/menu/" if domain else "http://127.0.0.1:8008/menu/"
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=2,
        )
        qr.add_data(url)
        qr.make(fit=True)
        img = qr.make_image(fill_color="#dfb256", back_color="#070c18")
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        self.permanent_qr_image.save("permanent_restaurant_qr.png", File(buffer), save=False)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.permanent_qr_image:
            self.generate_permanent_qr()
            super().save(update_fields=['permanent_qr_image'])


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    display_order = models.PositiveIntegerField(default=0)
    icon = models.CharField(max_length=50, default='fa-utensils', help_text="FontAwesome icon e.g. fa-cocktail, fa-beer, fa-utensils, fa-drumstick-bite")

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['display_order', 'name']

    def __str__(self):
        return self.name


class MenuItem(models.Model):
    DIET_CHOICES = [
        ('veg', 'Vegetarian (Veg)'),
        ('non_veg', 'Non-Vegetarian (Non-Veg)'),
        ('egg', 'Contains Egg'),
        ('beverage', 'Beverage / Drink'),
    ]

    category = models.ForeignKey(Category, related_name='items', on_delete=models.CASCADE)
    code = models.CharField(max_length=20, blank=True, null=True, help_text="Optional item code e.g. SC1, VC1, ST1")
    name = models.CharField(max_length=200)
    flavor_or_subtext = models.CharField(max_length=255, blank=True, null=True, help_text="Flavors, notes or serving options")
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, help_text="Price in INR (₹)")
    diet_type = models.CharField(max_length=20, choices=DIET_CHOICES, default='non_veg')
    is_available = models.BooleanField(default=True, help_text="Uncheck when item is Sold Out")
    is_featured = models.BooleanField(default=False, help_text="Highlight in chef special or featured section")
    image = models.ImageField(upload_to='menu_items/', blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['category__display_order', 'code', 'name']

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        try:
            from .pdf_generator import render_dynamic_pdf_pages
            render_dynamic_pdf_pages()
        except Exception as e:
            print(f"Error updating dynamic PDF: {e}")

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        try:
            from .pdf_generator import render_dynamic_pdf_pages
            render_dynamic_pdf_pages()
        except Exception as e:
            print(f"Error updating dynamic PDF: {e}")

    def __str__(self):
        status = "Available" if self.is_available else "Sold Out"
        return f"{self.name} - ₹{self.price} ({status})"


class MenuPage(models.Model):
    page_number = models.PositiveIntegerField(unique=True)
    title = models.CharField(max_length=100)
    image = models.CharField(max_length=255, help_text="Path in static, e.g. menu_pages/page_1.jpg")

    class Meta:
        ordering = ['page_number']

    def __str__(self):
        return f"Page {self.page_number} - {self.title}"


class TableQR(models.Model):
    table_number = models.CharField(max_length=50, unique=True, help_text="e.g. Table 1, Rooftop VIP 2, Bar Counter")
    qr_image = models.ImageField(upload_to='qr_codes/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def generate_qr(self, domain=""):
        url = f"{domain.rstrip('/')}/menu/?table={self.table_number}" if domain else f"http://127.0.0.1:8008/menu/?table={self.table_number}"
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=2,
        )
        qr.add_data(url)
        qr.make(fit=True)
        img = qr.make_image(fill_color="#dfb256", back_color="#070c18")

        buffer = BytesIO()
        img.save(buffer, format="PNG")
        file_name = f"qr_table_{self.table_number.replace(' ', '_').lower()}.png"
        self.qr_image.save(file_name, File(buffer), save=False)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.qr_image:
            self.generate_qr()
            super().save(update_fields=['qr_image'])

    def __str__(self):
        return f"QR for {self.table_number}"
