import os
from pathlib import Path
from dotenv import load_dotenv
import environ
import dj_database_url

# Load environment variables from a .env file
load_dotenv()
env = environ.Env()
environ.Env.read_env()

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent

TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates/')

# Secret key & debug
SECRET_KEY = os.environ.get('SECRET_KEY')  # fallback for dev only
DEBUG = os.environ.get('DEBUG', 'False') == 'True'

ALLOWED_HOSTS = ['*']

# Installed apps
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Allauth
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',

    # Your apps
    'core',
    'todo',
    'study_tracker',
    'users',
    'vault',
]

# Custom user model
AUTH_USER_MODEL = 'users.User'

# Middleware
MIDDLEWARE = [
    "allauth.account.middleware.AccountMiddleware",  # Must be before AuthenticationMiddleware
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Add this line
]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# URL config
ROOT_URLCONF = 'saas.urls'

# Templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATES_DIR],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',  # Required by allauth
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# WSGI
WSGI_APPLICATION = 'saas.wsgi.application'

# Authentication backends
AUTHENTICATION_BACKENDS = [
    'users.auth_backends.EmailBackend',  # Your custom backend
    'allauth.account.auth_backends.AuthenticationBackend',
]

# Allauth settings (update deprecated settings to recommended ones)
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True
ACCOUNT_LOGIN_ON_GET = True

# Replace deprecated ACCOUNT_AUTHENTICATION_METHOD, ACCOUNT_EMAIL_REQUIRED, ACCOUNT_USERNAME_REQUIRED with new:
ACCOUNT_LOGIN_METHODS = {'email'}
ACCOUNT_SIGNUP_FIELDS = ['email*', 'password1*', 'password2*']

ACCOUNT_EMAIL_VERIFICATION = 'optional'
SOCIALACCOUNT_ADAPTER = 'users.adapters.CustomSocialAccountAdapter'
SOCIALACCOUNT_LOGIN_ON_GET = True

# Login / Logout redirect URLs
LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'home'

# Google OAuth
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'APP': {
            'client_id': os.environ.get("GOOGLE_CLIENT_ID"),
            'secret': os.environ.get("GOOGLE_CLIENT_SECRET"),
            'key': ''
        }
    }
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


database_url = 'postgresql://nova_db_j9lt_user:ZaDNL0j8wqIMmyavKe8OS3jA55YXnH0D@dpg-d0sq272li9vc73d8t2m0-a.oregon-postgres.render.com/nova_db_j9lt'
DATABASES['default'] = dj_database_url.parse(database_url)

# Password validation (enable in production)
AUTH_PASSWORD_VALIDATORS = [
    # {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    # {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    # {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    # {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files
STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
# OpenAI API Key (for future use)
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

# Valut
YOUTUBE_API_KEY = os.environ.get('YOUTUBE_API_KEY')

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Email settings for notifications (example with console)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
DEFAULT_FROM_EMAIL = 'ichukwugozirim@gmail.com'
ADMINS = [('Admin', 'ichukwugozirim@gmail.com')]