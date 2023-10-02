from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = BASE_DIR / 'templates'

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-31sh+@f*(uu#3n8+oxbk6=#@hrjlu(e*4exjc2a4z)_9*^g45@'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ["*"]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'tracking',  # Tracking user visits and page views
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',

    # Our apps
    'website',
    'account',
    'facilities',
    'shop',
    'mailer',
    'mainapp',
    'superadmin',
    'api',  # Api app - handles all the api stuff
    'pharmacetical',
    'patient',
    'doctor',
    'interact',  # Interact app used in consultations

    # Third party
    'rest_framework',
    'corsheaders',
    'django_filters',
    'rest_framework_swagger',  # For making api documentation
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'tracking.middleware.VisitorTrackingMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

REST_FRAMEWORK = {'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema'}

ROOT_URLCONF = 'teleMedicine.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATES_DIR, ],
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

WSGI_APPLICATION = 'teleMedicine.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

if DEBUG:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db1.sqlite3',
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'mysql.connector.django',
            'NAME': '',  #  # d # d
            'USER': '',  #  # d
            'PASSWORD': '[',  # d-dRdQHapV[
            'HOST': 'localhost',
            'PORT': '3306',
        }
    }

# Email settings
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
# EMAIL_HOST_USER = 'sheerohkiragu@gmail.com'
# EMAIL_HOST_PASSWORD = 'rugnataqrwsxqiba'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'mail.resq247.life'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'no-reply@resq247.life'
DEFAULT_FROM_EMAIL = 'ResQ247 <no-reply@resq247.life>'
EMAIL_HOST_PASSWORD = 'G{(bYvnt$o&I'

ADMIN_EMAILS = ['resq247@gmail.com']

# CORS settings
# CORS_ALLOWED_ORIGINS = []
CORS_ALLOW_ALL_ORIGINS = True

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Africa/Nairobi'

USE_I18N = True

USE_TZ = True

# Tracking settings
TRACK_AJAX_REQUESTS = True
TRACK_ANONYMOUS_USERS = True
TRACK_SUPERUSERS = False
TRACK_PAGEVIEWS = True
TRACK_REFERER = True
TRACK_QUERY_STRING = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = 'staticfiles/'
STATICFILES_DIRS = [BASE_DIR / 'static', ]

if DEBUG:
    # Dev media storage
    MEDIA_URL = 'media/'
    MEDIA_ROOT = 'media/'
else:
    # Production media storage and routing
    MEDIA_ROOT = "/home/resqhdub/media.resq247.life/"
    MEDIA_URL = "http://media.resq247.life/"

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


