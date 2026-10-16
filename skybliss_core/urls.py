from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('menu.urls')),
]

from django.views.static import serve
from django.urls import re_path

urlpatterns += [
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.BASE_DIR / 'static'}),
]

admin.site.site_header = "Sky Bliss - The AeroPub Admin"
admin.site.site_title = "Sky Bliss Admin Portal"
admin.site.index_title = "Rooftop Lounge Menu & Pricing Management"
