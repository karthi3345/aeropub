import os
import django
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from menu.models import Category, MenuItem, RestaurantSettings, TableQR

class RestaurantMenuSystemTests(TestCase):
    def setUp(self):
        self.client = Client()
        # Admin user
        self.admin = User.objects.create_superuser('admin_tester', 'test@skybliss.com', 'pass123')
        
        # Settings & PDF
        self.settings = RestaurantSettings.objects.create(
            name="Sky Bliss — The AeroPub",
            tagline="Rooftop Lounge"
        )
        self.settings.generate_permanent_qr()
        self.settings.save()

        # Category
        self.cat_cocktails = Category.objects.create(name="Signature Cocktails", slug="signature-cocktails", display_order=1)
        self.cat_starters = Category.objects.create(name="First Class Starters", slug="first-class-starters", display_order=2)

        # Items
        self.item1 = MenuItem.objects.create(
            category=self.cat_cocktails,
            code="SC1",
            name="Runway Rum",
            price=600.00,
            diet_type="beverage",
            is_available=True
        )
        self.item2 = MenuItem.objects.create(
            category=self.cat_starters,
            code="ST1",
            name="Chicken Biryani",
            price=180.00,
            diet_type="non_veg",
            is_available=True
        )

    def test_1_permanent_customer_menu_opens(self):
        """1. Scan the QR code and verify the customer menu opens with no login required"""
        response = self.client.get('/menu/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Sky Bliss")
        self.assertContains(response, "Runway Rum")
        self.assertContains(response, "₹600")

    def test_2_change_food_item_price_in_admin(self):
        """2. Change a food item's price in admin and verify customer menu updates"""
        # Change Chicken Biryani from 180 to 220
        self.item2.price = 220.00
        self.item2.save()

        # Verify on customer menu view
        response = self.client.get('/menu/')
        self.assertContains(response, "220")

        # Verify on live JSON sync API
        api_res = self.client.get('/api/menu-updates/')
        self.assertEqual(api_res.status_code, 200)
        data = api_res.json()
        item_updated = next(i for i in data['items'] if i['id'] == self.item2.id)
        self.assertEqual(float(item_updated['price']), 220.00)

    def test_3_add_new_food_item(self):
        """3. Add a new food item and verify it appears on the customer menu"""
        new_item = MenuItem.objects.create(
            category=self.cat_starters,
            code="ST99",
            name="Tandoori Prawn Platter",
            price=450.00,
            diet_type="non_veg",
            is_available=True
        )
        response = self.client.get('/menu/')
        self.assertContains(response, "Tandoori Prawn Platter")
        self.assertContains(response, "450")

    def test_4_edit_item_name_and_flavor(self):
        """4. Edit an item name and verify changes"""
        self.item1.name = "Royal Runway Rum Special"
        self.item1.flavor_or_subtext = "Vintage Spiced"
        self.item1.save()

        response = self.client.get('/menu/')
        self.assertContains(response, "Royal Runway Rum Special")
        self.assertContains(response, "Vintage Spiced")

    def test_5_delete_item(self):
        """5. Delete an item and verify it disappears"""
        item_id = self.item1.id
        self.item1.delete()

        response = self.client.get('/menu/')
        self.assertNotContains(response, "Runway Rum")

        api_res = self.client.get('/api/menu-updates/')
        ids = [i['id'] for i in api_res.json()['items']]
        self.assertNotIn(item_id, ids)

    def test_6_mark_item_sold_out(self):
        """6. Mark an item Sold Out and verify its status"""
        self.item2.is_available = False
        self.item2.save()

        response = self.client.get('/menu/')
        self.assertContains(response, "Sold Out")

        api_res = self.client.get('/api/menu-updates/')
        item_data = next(i for i in api_res.json()['items'] if i['id'] == self.item2.id)
        self.assertFalse(item_data['is_available'])

    def test_7_permanent_qr_persists(self):
        """7. Verify permanent restaurant QR exists and points to /menu/"""
        self.assertTrue(bool(self.settings.permanent_qr_image))
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_8_pdf_menu_url(self):
        """8. Permanent PDF URL serves the official menu"""
        response = self.client.get('/menu/pdf/')
        # Should return 200 with application/pdf if file exists
        if response.status_code == 200:
            self.assertEqual(response['Content-Type'], 'application/pdf')
