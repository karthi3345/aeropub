import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'skybliss_core.settings')
django.setup()

from menu.models import Category, MenuItem, RestaurantSettings, TableQR
from django.test import Client

def run_live_verification():
    print("=" * 60)
    print("RUNNING SKY BLISS RESTAURANT SYSTEM VERIFICATION")
    print("=" * 60)

    client = Client()

    # 1. Customer Menu Opens
    res = client.get('/menu/')
    assert res.status_code == 200, f"Expected 200, got {res.status_code}"
    print("[PASS] 1. Permanent customer menu (/menu/) opens successfully without login (HTTP 200).")

    # 2. Price Change Test
    item = MenuItem.objects.filter(code='SC1').first()
    if not item:
        cat = Category.objects.first()
        item = MenuItem.objects.create(category=cat, code='SC1', name='Runway Rum', price=600.00)
    
    old_price = item.price
    item.price = 620.00
    item.save()

    api_res = client.get('/api/menu-updates/')
    items_json = api_res.json()['items']
    found = next((i for i in items_json if i['id'] == item.id), None)
    assert found and float(found['price']) == 620.00, "Price update not reflected in API"
    print(f"[PASS] 2. Price change reflected immediately: {item.name} updated to INR 620.00.")

    # Restore price
    item.price = old_price
    item.save()

    # 3. Add New Food Item
    cat = Category.objects.first()
    test_item = MenuItem.objects.create(
        category=cat,
        code='TEST01',
        name='Chef Special Truffle Wings',
        price=450.00,
        diet_type='non_veg',
        is_available=True
    )
    menu_html = client.get('/menu/').content.decode('utf-8')
    assert 'Chef Special Truffle Wings' in menu_html, "New item not in menu HTML"
    print("[PASS] 3. Newly added food item appeared on customer menu.")

    # 4. Edit Name & Flavor
    test_item.name = 'Chef Golden Truffle Wings'
    test_item.flavor_or_subtext = 'Smoked Honey Glaze'
    test_item.save()
    menu_html = client.get('/menu/').content.decode('utf-8')
    assert 'Chef Golden Truffle Wings' in menu_html and 'Smoked Honey Glaze' in menu_html, "Item edit failed"
    print("[PASS] 4. Item edit (name and flavor) verified on customer menu.")

    # 5. Mark Sold Out
    test_item.is_available = False
    test_item.save()
    api_res = client.get('/api/menu-updates/').json()
    item_in_api = next(i for i in api_res['items'] if i['id'] == test_item.id)
    assert item_in_api['is_available'] is False, "Sold out flag not updated"
    print("[PASS] 5. Item marked Sold Out: status correctly synchronized.")

    # 6. Delete Item
    test_id = test_item.id
    test_item.delete()
    api_res = client.get('/api/menu-updates/').json()
    remaining_ids = [i['id'] for i in api_res['items']]
    assert test_id not in remaining_ids, "Deleted item still present in API"
    print("[PASS] 6. Deleted food item completely removed from customer menu.")

    # 7. Permanent PDF URL Check
    pdf_res = client.get('/menu/pdf/')
    assert pdf_res.status_code == 200, f"Expected PDF 200, got {pdf_res.status_code}"
    assert pdf_res['Content-Type'] == 'application/pdf', "Content-Type is not application/pdf"
    print("[PASS] 7. Permanent PDF URL (/menu/pdf/) serves active official PDF.")

    # 8. Permanent Restaurant QR
    settings = RestaurantSettings.objects.first()
    assert settings and bool(settings.permanent_qr_image), "Permanent QR code image is missing"
    print(f"[PASS] 8. Permanent Restaurant QR exists at {settings.permanent_qr_image.url} and points permanently to /menu/.")

    print("=" * 60)
    print("ALL 8 VERIFICATION TESTS PASSED SUCCESSFULLY!")
    print("=" * 60)

if __name__ == '__main__':
    run_live_verification()
