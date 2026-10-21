import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Local development values live in backend/local_settings.py (never commit it).
# On a live server, set the same names as environment variables instead.
try:
    from . import local_settings as _local
except ImportError:
    _local = None


def setting(name, default=None):
    """Environment variable first, then local_settings.py, then the default."""
    if name in os.environ:
        return os.environ[name]
    return getattr(_local, name, default)


def as_list(value):
    return [item.strip() for item in str(value or '').split(',') if item.strip()]


SECRET_KEY = setting('SECRET_KEY')
if not SECRET_KEY:
    raise Exception('Set SECRET_KEY as an environment variable or in backend/local_settings.py')

# Safe default is False. Add DEBUG = True to local_settings.py for development.
DEBUG = str(setting('DEBUG', 'False')).lower() in ('true', '1')

ALLOWED_HOSTS = as_list(setting('ALLOWED_HOSTS', '127.0.0.1,localhost'))
# Render sets this variable automatically for web services.
RENDER_HOST = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_HOST:
    ALLOWED_HOSTS.append(RENDER_HOST)

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'buddies_api',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # must stay first
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # serves static files in production
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'backend.urls'
WSGI_APPLICATION = 'backend.wsgi.application'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

# On Render, DATABASE_URL points at the PostgreSQL database.
# Locally (no DATABASE_URL) the MySQL values from local_settings.py are used.
DATABASE_URL = setting('DATABASE_URL')
if DATABASE_URL:
    import dj_database_url
    DATABASES = {'default': dj_database_url.parse(DATABASE_URL, conn_max_age=600)}
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': setting('DB_NAME'),
            'USER': setting('DB_USER'),
            'PASSWORD': setting('DB_PASSWORD'),
            'HOST': setting('DB_HOST', '127.0.0.1'),
            'PORT': setting('DB_PORT', '3306'),
        }
    }

# React origins allowed to call the API. Add your live site address on the server,
# e.g. CORS_ALLOWED_ORIGINS=https://your-site.netlify.app
CORS_ALLOWED_ORIGINS = as_list(setting('CORS_ALLOWED_ORIGINS', 'http://localhost:3000'))
# Needed for the /admin/ login on https, e.g. https://your-backend.example.com
CSRF_TRUSTED_ORIGINS = as_list(setting('CSRF_TRUSTED_ORIGINS', ''))
if RENDER_HOST:
    CSRF_TRUSTED_ORIGINS.append(f'https://{RENDER_HOST}')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
TIME_ZONE = 'Asia/Kolkata'
USE_TZ = True

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'  # collectstatic in build.sh writes here
STORAGES = {
    'default': {'BACKEND': 'django.core.files.storage.FileSystemStorage'},
    'staticfiles': {'BACKEND': 'whitenoise.storage.CompressedStaticFilesStorage'},
}

if DEBUG:
    # Lets an older local MySQL build work during development only.
    from django.db.backends.base.base import BaseDatabaseWrapper
    BaseDatabaseWrapper.check_database_version_supported = lambda self: None
else:
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    # JSON only: no browsable API page on the live site.
    REST_FRAMEWORK = {
        'DEFAULT_RENDERER_CLASSES': ['rest_framework.renderers.JSONRenderer'],
    }