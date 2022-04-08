import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-*7vnz0p_b9=vjc6!w97*20=shvy$#klz2k+=+51y_7+l8!^&57'

DEBUG = True

ALLOWED_HOSTS = ['cozastore123.herokuapp.com', '127.0.0.1']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
     'whitenoise',
    'django.contrib.staticfiles',
    
    'MClothing.apps.MclothingConfig',
    'MBasket.apps.MbasketConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'DVanezStore.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR.joinpath('templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages', #It allows to be accessible from all the pages
                'MClothing.context_processors.categories',
                'MClothing.context_processors.get_filters',
                'MBasket.context_processors.basket',
            ],
        },
    },
]

WSGI_APPLICATION = 'DVanezStore.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}



'''
DATABASES = {
    'default': {
    'ENGINE': 'django.db.backends.postgresql',
    'NAME': 'cozastore',
    'USER': 'postgres',
    'PASSWORD': 'ProgrammerGodRobo123',
    'HOST': 'localhost',
    'PORT': '5432',
    }
}

'''

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


LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


STATIC_URL = '/staticfiles/'  
STATICFILES_DIRS=[         
    os.path.join(BASE_DIR, 'staticfiles')  
    ]

STATIC_ROOT=os.path.join(BASE_DIR, 'static')

#FOR SAVING IMAGES INTO THE 'static/images'
MEDIA_URL ='/mediafiles/'  #your url path
MEDIA_ROOT =os.path.join(BASE_DIR, 'staticfiles/mediafiles')  


#WHITENOISE CONFIGURATION
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'

#For some reasson this doesn't work
#STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
