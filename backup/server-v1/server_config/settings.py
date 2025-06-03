import os
from decouple import config

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config("SECRET_KEY")


ROOT_URLCONF = 'server_config.urls'

CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", "amqp://guest:guest@rabbitmq:5672//")
CELERY_RESULT_BACKEND = "django-db"
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

INSTALLED_APPS += [
    'django_prometheus',
    'django_celery_results',
    'django_celery_beat',
    'weather',
    'corsheaders',  # Ajouté ici directement
]

from decouple import config

#DATABASES = {
#    'default': {
#       'ENGINE': 'django.db.backends.postgresql',
#        'NAME': os.getenv('POSTGRES_DB', 'devops_db'),
#        'USER': os.getenv('POSTGRES_USER', 'devops_user'),
#        'PASSWORD': os.getenv('POSTGRES_PASSWORD', 'devops_pass'),
#        'HOST': os.getenv('POSTGRES_HOST', 'localhost'),
#        'PORT': 5432,
#    }
#}

#DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.postgresql',
#        'NAME': 'mydb',
#        'USER': 'postgres',
#        'PASSWORD': 'postgres',
#        'HOST': 'localhost',
#        'PORT': 5432,
#    }
#}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',  # Fichier de base de données à la racine du projet
    }
}



OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")


ALLOWED_HOSTS = ['*']
CORS_ALLOW_ALL_ORIGINS = True

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Ajouter CorsMiddleware en premier dans la liste middleware
MIDDLEWARE = ["corsheaders.middleware.CorsMiddleware"] + MIDDLEWARE

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],  # tu peux ajouter ici tes dossiers de templates si tu en as
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',  # important pour admin
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
DEBUG = os.getenv("DEBUG", "False") == "True"

STATIC_URL = '/static/'

# For development (optional)
STATICFILES_DIRS = [BASE_DIR / "static"]

# For production (optional, used with collectstatic)
STATIC_ROOT = BASE_DIR / "staticfiles"