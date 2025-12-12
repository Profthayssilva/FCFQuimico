"""
Django settings for FCF project.
Production-ready configuration for Render
"""

from pathlib import Path
import os

# ============================
# BASE
# ============================
BASE_DIR = Path(__file__).resolve().parent.parent


# ============================
# SEGURANÇA
# ============================
SECRET_KEY = os.environ.get(
    "DJANGO_SECRET_KEY",
    "django-insecure-hcg&z$!gjh^=^t73z_@61qc1)7vwerif6#_37*%ei@3j*o1e+t"
)

DEBUG = False

ALLOWED_HOSTS = [
    "fcfquimicos.onrender.com",
    ".onrender.com",
]


# ============================
# APLICAÇÕES
# ============================
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core',
]


# ============================
# MIDDLEWARE
# ============================
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',

    # 🔹 necessário para static no Render
    'whitenoise.middleware.WhiteNoiseMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


# ============================
# URL / WSGI
# ============================
ROOT_URLCONF = 'FCF.urls'
WSGI_APPLICATION = 'FCF.wsgi.application'


# ============================
# TEMPLATES
# ============================
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


# ============================
# BANCO DE DADOS
# ============================
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# ============================
# INTERNACIONALIZAÇÃO
# ============================
LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_TZ = True


# ============================
# ARQUIVOS ESTÁTICOS (CRÍTICO)
# ============================
STATIC_URL = '/static/'

STATICFILES_DIRS = [
    BASE_DIR / 'core' / 'static'
]

STATIC_ROOT = BASE_DIR / 'staticfiles'

# 🔹 Whitenoise
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# ============================
# MEDIA
# ============================
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


# ============================
# PADRÃO
# ============================
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# ============================
# EMAIL (GMAIL)
# ============================
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True

EMAIL_HOST_USER = "contatofcfquimicos@gmail.com"
EMAIL_HOST_PASSWORD = "lzof vomz qhaj vjpo"

DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
