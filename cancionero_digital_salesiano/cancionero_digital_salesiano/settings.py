"""
Django settings for cancionero_digital_salesiano project.

Generado por 'django-admin startproject'.
"""

from pathlib import Path
import os  # Para manejar rutas del sistema

# ============================
# 📁 BASE DEL PROYECTO
# ============================

BASE_DIR = Path(__file__).resolve().parent.parent

# ============================
# 🔐 SEGURIDAD BÁSICA
# ============================

SECRET_KEY = 'django-insecure-%3%+a1i61)7k5*%16878+a!d9b4!4e4_9b_+gct-798hi68bvx'
DEBUG = True  # Cambiar a False en producción
ALLOWED_HOSTS = []  # Añadir dominios permitidos en producción

# ============================
# 🧩 APLICACIONES INSTALADAS
# ============================

INSTALLED_APPS = [
    # Django apps básicas
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Nuestra app
    'canciones',

    # Autenticación avanzada
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',

    # Formularios estilizados con Bootstrap 5
    'crispy_forms',
    'crispy_bootstrap5',
]

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

# ============================
# 🧱 MIDDLEWARE
# ============================

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # Middleware de allauth (gestión de cuentas)
    "allauth.account.middleware.AccountMiddleware",

    # Middleware para traducciones
    'django.middleware.locale.LocaleMiddleware',
]

# ============================
# 🌐 CONFIGURACIÓN DE RUTAS
# ============================

ROOT_URLCONF = 'cancionero_digital_salesiano.urls'

# ============================
# 🖼 TEMPLATES (HTML)
# ============================

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),  # Plantillas globales
            os.path.join(BASE_DIR, 'canciones', 'templates'),  # Plantillas específicas de la app
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',  # Necesario para allauth
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# ============================
# 🔐 BACKENDS DE AUTENTICACIÓN
# ============================

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',  # Para admin y login clásico
    'allauth.account.auth_backends.AuthenticationBackend',  # Para login con email o usuario
]

# ============================
# 🚀 WSGI
# ============================

WSGI_APPLICATION = 'cancionero_digital_salesiano.wsgi.application'

# ============================
# 🗄 BASE DE DATOS (PostgreSQL)
# ============================

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'cancionero_db',
        'USER': 'programador',
        'PASSWORD': 'tfg.programador.25',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# ============================
# 🔒 VALIDACIÓN DE CONTRASEÑAS
# ============================

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ============================
# 🌍 INTERNACIONALIZACIÓN
# ============================

LANGUAGE_CODE = 'es'  # Idioma por defecto: Español
TIME_ZONE = 'UTC'     # Puedes cambiarlo a tu zona (ej. 'Europe/Madrid')
USE_I18N = True
USE_TZ = True

# ============================
# 🖼 ARCHIVOS ESTÁTICOS
# ============================

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / "static",  # Carpeta global de archivos estáticos (CSS, JS, imágenes)
]

# ============================
# 🔑 CONFIGURACIÓN DE LLAVES PRIMARIAS
# ============================

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ============================
# 📧 BACKEND DE EMAIL (DESARROLLO)
# ============================

if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# En producción usar SMTP, Amazon SES, etc.

# ============================
# ⚙️ CONFIGURACIÓN DE ALLAUTH
# ============================

ACCOUNT_AUTHENTICATED_LOGIN_REDIRECTS = True  # Redirige automáticamente al home después de login

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
SIGNUP_REDIRECT_URL = '/'

ACCOUNT_LOGIN_METHODS = {"username", "email"}     # Permite login por username o email
ACCOUNT_SIGNUP_FIELDS = ["email*", "username*", "password1*", "password2*"]  # Campos requeridos para registro
ACCOUNT_UNIQUE_EMAIL = True                       # No se permiten dos cuentas con el mismo email

ACCOUNT_RATE_LIMITS = {
    "login_failed": "5/5m",  # Máximo 5 intentos fallidos cada 5 minutos
}

ACCOUNT_SESSION_REMEMBER = True                   # Mantiene la sesión iniciada
ACCOUNT_CONFIRM_EMAIL_ON_GET = True               # Confirmación automática al hacer clic en el link del email
ACCOUNT_EMAIL_VERIFICATION = "mandatory"          # Verificación de email obligatoria
ACCOUNT_EMAIL_SUBJECT_PREFIX = "Cancionero Salesiano"  # Prefijo de los emails
ACCOUNT_PRESERVE_USERNAME_CASING = False          # Convierte nombres de usuario a minúsculas
