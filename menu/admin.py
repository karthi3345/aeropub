from django.contrib import admin
from .models import Category, MenuItem, TableQR, MenuPage, RestaurantSettings
from django.utils.html import format_html
from django.utils.safestring import mark_safe

@admin.register(RestaurantSettings)
class RestaurantSettingsAdmin(admin.ModelAdmin):
    list_display = ('name', 'pdf_status', 'permanent_qr_preview', 'menu_link', 'pdf_updated_at')
    fields = ('name', 'tagline', 'menu_pdf', 'permanent_qr_preview')
    readonly_fields = ('permanent_qr_preview',)

    def pdf_status(self, obj):
        if obj.menu_pdf:
            return mark_safe('<a href="/menu/pdf/" target="_blank" style="color:#10b981; font-weight:600;"><i class="fa fa-file-pdf"></i> View Active PDF Menu</a>')
        return mark_safe('<span style="color:#ef4444;">No PDF Uploaded</span>')
    pdf_status.short_description = "Active PDF Menu"

    def permanent_qr_preview(self, obj):
        if obj.permanent_qr_image:
            return format_html(
                '<div><img src="{}" style="max-height: 120px; border-radius: 8px; border: 2px solid #dfb256;" /><br>'
                '<a href="{}" download="skybliss_restaurant_qr.png" class="button" style="margin-top:6px; display:inline-block; background:#dfb256; color:#070c18; font-weight:bold; padding:4px 8px; border-radius:4px; text-decoration:none;">Download Permanent QR</a></div>',
                obj.permanent_qr_image.url, obj.permanent_qr_image.url
            )
        return "No QR Generated"
    permanent_qr_preview.short_description = "Permanent Restaurant QR"

    def menu_link(self, obj):
        return mark_safe('<a href="/menu/" target="_blank" style="background:#070c18; color:#dfb256; padding:4px 10px; border-radius:4px; text-decoration:none; border:1px solid #dfb256;">Open Customer Menu</a>')
    menu_link.short_description = "Permanent Menu Link"

    def has_add_permission(self, request):
        # Enforce singleton settings
        return not RestaurantSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'display_order', 'item_count', 'icon_display')
    list_editable = ('display_order',)
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)

    def item_count(self, obj):
        return obj.items.count()
    item_count.short_description = "Items in Category"

    def icon_display(self, obj):
        return format_html('<i class="fa-solid {}" style="font-size: 1.1rem; color:#dfb256;"></i> {}', obj.icon, obj.icon)
    icon_display.short_description = "Category Icon"


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'category', 'price_display', 'diet_badge', 'is_available', 'is_featured', 'image_thumb', 'updated_at')
    list_filter = ('category', 'is_available', 'diet_type', 'is_featured')
    search_fields = ('name', 'code', 'flavor_or_subtext', 'description')
    list_editable = ('is_available', 'is_featured')
    list_per_page = 25
    save_on_top = True

    fieldsets = (
        ('Dish Identification', {
            'fields': ('category', 'code', 'name', 'diet_type', 'flavor_or_subtext', 'description')
        }),
        ('Live Pricing & Status', {
            'fields': ('price', 'is_available', 'is_featured'),
            'description': 'Price changes and availability (Sold Out vs Available) immediately synchronize with customer QR menus.'
        }),
        ('Dish Photography', {
            'fields': ('image',),
            'description': 'Upload photo of this item. If not provided, category aesthetic icon is displayed gracefully.'
        }),
    )

    def price_display(self, obj):
        return format_html(
            '<div class="flex items-center gap-1 font-mono font-bold text-emerald-400 text-sm">'
            '<span class="text-xs text-emerald-500/70 font-sans">₹</span><span>{}</span>'
            '</div>', 
            obj.price
        )
    price_display.short_description = "Price"
    price_display.admin_order_field = 'price'

    def diet_badge(self, obj):
        if obj.diet_type == 'veg':
            return mark_safe(
                '<span class="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-xs font-semibold bg-emerald-950/60 text-emerald-400 border border-emerald-500/40">'
                '<span class="h-1.5 w-1.5 rounded-full bg-emerald-400"></span>VEG</span>'
            )
        elif obj.diet_type == 'egg':
            return mark_safe(
                '<span class="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-xs font-semibold bg-amber-950/60 text-amber-300 border border-amber-500/40">'
                '<span class="h-1.5 w-1.5 rounded-full bg-amber-400"></span>EGG</span>'
            )
        elif obj.diet_type == 'beverage':
            return mark_safe(
                '<span class="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-xs font-semibold bg-sky-950/60 text-sky-300 border border-sky-500/40">'
                '<i class="fa-solid fa-cocktail text-[10px]"></i>DRINK</span>'
            )
        return mark_safe(
            '<span class="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-xs font-semibold bg-rose-950/60 text-rose-400 border border-rose-500/40">'
            '<span class="h-1.5 w-1.5 rounded-full bg-rose-500"></span>NON-VEG</span>'
        )
    diet_badge.short_description = "Diet"

    def image_thumb(self, obj):
        if obj.image:
            try:
                return format_html(
                    '<div class="relative group w-11 h-11 rounded-lg overflow-hidden border border-amber-500/30 shadow-md bg-slate-900">'
                    '<img src="{}" class="w-full h-full object-cover transition-transform group-hover:scale-110" />'
                    '</div>', 
                    obj.image.url
                )
            except Exception:
                pass
        return mark_safe(
            '<div class="w-11 h-11 rounded-lg border border-slate-700/60 bg-slate-800/40 flex items-center justify-center text-slate-500 text-xs">'
            '<i class="fa-solid fa-camera text-sm"></i>'
            '</div>'
        )
    image_thumb.short_description = "Photo"


@admin.register(TableQR)
class TableQRAdmin(admin.ModelAdmin):
    list_display = ('table_number', 'qr_preview', 'menu_link', 'created_at')
    search_fields = ('table_number',)

    def qr_preview(self, obj):
        if obj.qr_image:
            return format_html(
                '<a href="{}" target="_blank"><img src="{}" style="max-height: 65px; border-radius: 6px; border: 1px solid #dfb256;" /></a><br>'
                '<a href="{}" download="qr_{}.png" style="font-size:0.75rem; color:#dfb256;">Download</a>',
                obj.qr_image.url, obj.qr_image.url, obj.qr_image.url, obj.table_number.replace(' ', '_').lower()
            )
        return "No QR Generated"
    qr_preview.short_description = "Table QR (Download/Print)"

    def menu_link(self, obj):
        return format_html('<a class="button" href="/menu/?table={}" target="_blank" style="background:#070c18; color:#dfb256; padding:4px 10px; border-radius:4px; text-decoration:none; border:1px solid #dfb256;">Open Table Menu</a>', obj.table_number)
    menu_link.short_description = "Table Link"


@admin.register(MenuPage)
class MenuPageAdmin(admin.ModelAdmin):
    list_display = ('page_number', 'title', 'page_preview')
    ordering = ('page_number',)

    def page_preview(self, obj):
        url = f"/static/{obj.image}"
        return format_html('<a href="{}" target="_blank"><img src="{}" style="height: 60px; border-radius: 4px; border: 1px solid #dfb256;" /></a>', url, url)
    page_preview.short_description = "Page Preview"
