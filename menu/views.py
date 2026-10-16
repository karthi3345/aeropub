from django.shortcuts import render
from django.http import JsonResponse, FileResponse, Http404
from .models import Category, MenuItem, TableQR, MenuPage, RestaurantSettings
from django.db.models import Prefetch
import os

import base64
from io import BytesIO
import qrcode

def qr_landing_view(request):
    """
    First Screen: Displays ONLY the official Permanent Restaurant QR Code standee.
    Renders an inline Base64 Data URI so the QR code is 100% self-contained and never shows a broken image link.
    """
    settings = RestaurantSettings.objects.first()
    menu_url = request.build_absolute_uri('/menu/')
    
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=2,
    )
    qr.add_data(menu_url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="#dfb256", back_color="#070c18")
    
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    qr_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    qr_data_uri = f"data:image/png;base64,{qr_base64}"
    
    return render(request, 'menu/qr_stand.html', {
        'settings': settings,
        'qr_data_uri': qr_data_uri,
        'menu_url': menu_url
    })

def customer_menu_view(request):
    """
    Customer Menu (/menu/):
    Opened after scanning the QR code.
    Shows the authentic PDF menu booklet with interactive page jump & real-time live database updates.
    """
    table = request.GET.get('table', 'General Guest')
    settings = RestaurantSettings.objects.first()
    pages = MenuPage.objects.all().order_by('page_number')

    categories = Category.objects.prefetch_related(
        Prefetch('items', queryset=MenuItem.objects.all().order_by('code', 'name'))
    ).all()

    context = {
        'settings': settings,
        'pages': pages,
        'categories': categories,
        'table': table,
        'total_pages': pages.count(),
        'total_items_count': MenuItem.objects.count(),
    }
    return render(request, 'menu/pdf_menu.html', context)

def digital_menu_grid_view(request):
    """
    Alternative interactive grid view of the menu
    """
    table = request.GET.get('table', 'General Guest')
    settings = RestaurantSettings.objects.first()

    categories = Category.objects.prefetch_related(
        Prefetch('items', queryset=MenuItem.objects.all().order_by('code', 'name'))
    ).all()

    context = {
        'settings': settings,
        'categories': categories,
        'table': table,
        'total_items_count': MenuItem.objects.count(),
    }
    return render(request, 'menu/digital_menu.html', context)

def download_active_pdf(request):
    """
    Permanent URL for downloading the official PDF file
    """
    settings = RestaurantSettings.objects.first()
    if settings and settings.menu_pdf and os.path.exists(settings.menu_pdf.path):
        return FileResponse(open(settings.menu_pdf.path, 'rb'), content_type='application/pdf')
    
    default_path = r'C:\Users\Karthik_Raja\Downloads\Menu card - Final version.pdf'
    if os.path.exists(default_path):
        return FileResponse(open(default_path, 'rb'), content_type='application/pdf')

    raise Http404("PDF menu is currently not available.")

def api_menu_updates(request):
    """
    Live real-time polling endpoint for PostgreSQL price changes
    """
    items_qs = MenuItem.objects.select_related('category').all()
    items_data = []

    for item in items_qs:
        image_url = item.image.url if item.image else None
        items_data.append({
            'id': item.id,
            'category_id': item.category_id,
            'category_slug': item.category.slug,
            'code': item.code or '',
            'name': item.name,
            'price': str(item.price),
            'formatted_price': f"₹{int(item.price) if item.price % 1 == 0 else item.price}",
            'diet_type': item.diet_type,
            'flavor_or_subtext': item.flavor_or_subtext or '',
            'description': item.description or '',
            'is_available': item.is_available,
            'is_featured': item.is_featured,
            'image_url': image_url,
            'updated_at': item.updated_at.isoformat()
        })

    return JsonResponse({
        'status': 'ok',
        'count': len(items_data),
        'items': items_data
    })
