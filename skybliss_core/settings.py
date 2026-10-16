import os
from pathlib import Path
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-skybliss-aeropub-secret-key-2026-key')

DEBUG = True

ALLOWED_HOSTS = ['*', '.vercel.app']

INSTALLED_APPS = [
    'unfold',
    'unfold.contrib.filters',
    'unfold.contrib.forms',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'whitenoise.runserver_nostatic',
    'cloudinary_storage',
    'django.contrib.staticfiles',
    'cloudinary',
    'menu',
]

UNFOLD = {
    "SITE_TITLE": "AeroPub Admin",
    "SITE_HEADER": "AeroPub Management",
    "SITE_URL": "/menu/",
    "SITE_ICON": {
        "light": lambda request: "/static/favicon.ico",
        "dark": lambda request: "/static/favicon.ico",
    },
    "DASHBOARD_CALLBACK": None,
    "STYLES": [
        lambda request: "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css",
    ],
    "COLORS": {
        "primary": {
            "50": "254 243 199",
            "100": "253 230 138",
            "200": "252 211 77",
            "300": "245 158 11",
            "400": "217 119 6",
            "500": "223 178 86",  # AeroPub Signature Gold
            "600": "198 153 59",
            "700": "161 115 37",
            "800": "120 83 23",
            "900": "84 57 15",
            "950": "49 31 6",
        },
    },
    "SIDEBAR": {
        "show_search": True,
        "show_all_applications": True,
        "navigation": [
            {
                "title": "Restaurant Management",
                "separator": True,
                "collapsible": False,
                "items": [
                    {
                        "title": "Menu Items (Dishes)",
                        "icon": "restaurant_menu",
                        "link": lambda request: "/admin/menu/menuitem/",
                    },
                    {
                        "title": "Categories",
                        "icon": "category",
                        "link": lambda request: "/admin/menu/category/",
                    },
                    {
                        "title": "Settings & PDF Upload",
                        "icon": "tune",
                        "link": lambda request: "/admin/menu/restaurantsettings/",
                    },
                    {
                        "title": "Table QR Codes",
                        "icon": "qr_code_2",
                        "link": lambda request: "/admin/menu/tableqr/",
                    },
                ],
            },
            {
                "title": "Quick Actions",
                "separator": True,
                "collapsible": False,
                "items": [
                    {
                        "title": "View Customer Menu",
                        "icon": "open_in_new",
                        "link": "/menu/",
                    },
                    {
                        "title": "Print Table QR Standee",
                        "icon": "print",
                        "link": "/menu/qr-stand/",
                    },
                ],
            },
        ],
    },
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'skybliss_core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'skybliss_core.wsgi.application'

# PostgreSQL (Neon DB Cloud instance or env override)
DATABASE_URL = os.environ.get(
    'DATABASE_URL', 
    'postgresql://neondb_owner:npg_s8euPTpOIyv0@ep-polished-king-b55e3ayh-pooler.c-7.us-east-2.aws.neon.tech/neondb?sslmode=require&channel_binding=require'
)

DATABASES = {
    'default': dj_database_url.config(
        default=DATABASE_URL,
        conn_max_age=600,
        ssl_require=True
    )
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Cloudinary Storage Configuration for Vercel & Production
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.environ.get('CLOUDINARY_CLOUD_NAME', 'a9it9xkq'),
    'API_KEY': os.environ.get('CLOUDINARY_API_KEY', '163812281322635'),
    'API_SECRET': os.environ.get('CLOUDINARY_API_SECRET', '2mS6EEUhi6YBlNMYRux4m39kOro'),
}

DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
