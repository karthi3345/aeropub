from django.urls import path
from . import views

urlpatterns = [
    # First screen: ONLY the QR code standee
    path('', views.qr_landing_view, name='home_qr'),
    path('qr/', views.qr_landing_view, name='qr_stand'),

    # Once scanned: What is in the PDF menu booklet comes up!
    path('menu/', views.customer_menu_view, name='customer_menu'),
    path('menu/grid/', views.digital_menu_grid_view, name='digital_menu_grid'),

    # Permanent URL for active PDF menu file
    path('menu/pdf/', views.download_active_pdf, name='download_active_pdf'),

    # Live synchronization API
    path('api/menu-updates/', views.api_menu_updates, name='api_menu_updates'),
]
