"""
Django settings for RLNClothes project.

Unified settings file for all environments (Prod, Hmg, Dev).
Controlled via environment variables (.env).
"""

from pathlib import Path
import os
import locale
from dotenv import load_dotenv

# Carrega variáveis do arquivo .env
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY", "django-insecure-CHANGE-ME-IN-PROD")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

# ALLOWED_HOSTS: Separados por vírgula no .env
# Ex: localhost,127.0.0.1,.fly.dev
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "localhost,127.0.0.1").split(",")

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_tables2",
    "django.contrib.humanize",
    "django_filters",
    "crispy_forms",
    "crispy_bootstrap4",
    "clientes.apps.ClientesConfig",
    "pedidos.apps.PedidosConfig",
    "fornecedores.apps.FornecedoresConfig",
    "notasfiscais.apps.NotasfiscaisConfig",
    "vendas.apps.VendasConfig",
    "pagamentos.apps.PagamentosConfig",
    "consultas.apps.ConsultasConfig",
]

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap4"
CRISPY_TEMPLATE_PACK = "bootstrap4"

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "rlnclothes.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "rlnclothes.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

import sys

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("DB_NAME", "rlnclothesdb"),
        "USER": os.getenv("DB_USER", "rlnclothesuser"),
        "PASSWORD": os.getenv("DB_PASSWORD", "rlnclothes"),
        "HOST": os.getenv("DB_HOST", "localhost"),
        "PORT": os.getenv("DB_PORT", "5432"),
    }
}

# Se estiver rodando testes (manage.py test OU pytest), usa SQLite em memória
if 'test' in sys.argv or any('pytest' in arg for arg in sys.argv):
    DATABASES['default'] = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / "db_test.sqlite3",
    }
    
    # Isso instrui o Django a não procurar por arquivos em 'migrations/',
    # mas sim criar as tabelas diretamente baseadas no código dos models.py
    class DisableMigrations:
        def __contains__(self, item):
            return True
        def __getitem__(self, item):
            return None

    MIGRATION_MODULES = DisableMigrations()

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

# LANGUAGE_CODE = "en-us"
LANGUAGE_CODE = "pt-br"

LOCALE_NAME = "pt_BR"

TIME_ZONE = "UTC"

USE_I18N = False

USE_L10N = True

USE_TZ = True

DECIMAL_SEPARATOR = ","

USE_DECIMAL_SEPARATOR = True

THOUSAND_SEPARATOR = "."

USE_THOUSAND_SEPARATOR = True

NUMBER_GROUPING = 3

DATETIME_FORMAT = "%d/%m/%Y"

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = "static/"
STATICFILES_DIRS = [
    BASE_DIR / "static",
]

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

LOGOUT_REDIRECT_URL = "/"

# Force managed=True for unmanaged models during tests
TEST_RUNNER = 'test_utils.runner.ManagedModelTestRunner'
