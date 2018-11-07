import os

import environ
root = environ.Path(__file__) - 3 # three folder back (/a/b/c/ - 3 = /)
env = environ.Env(DEBUG=(bool, False),) # set default values and casting
environ.Env.read_env() # reading .env file


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
#/home/m/Desktop/tutorial
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!

# SECRET_KEY = os.environ['SECRET_KEY']
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
if DEBUG:
   INTERNAL_IPS = ('127.0.0.1', 'localhost',)

   DEBUG_TOOLBAR_PANELS = [
       'debug_toolbar.panels.versions.VersionsPanel',
       'debug_toolbar.panels.timer.TimerPanel',
       'debug_toolbar.panels.settings.SettingsPanel',
       'debug_toolbar.panels.headers.HeadersPanel',
       'debug_toolbar.panels.request.RequestPanel',
       'debug_toolbar.panels.sql.SQLPanel',
       'debug_toolbar.panels.staticfiles.StaticFilesPanel',
       'debug_toolbar.panels.templates.TemplatesPanel',
       'debug_toolbar.panels.cache.CachePanel',
       'debug_toolbar.panels.signals.SignalsPanel',
       'debug_toolbar.panels.logging.LoggingPanel',
       'debug_toolbar.panels.redirects.RedirectsPanel',
   ]
ALLOWED_HOSTS = ['127.0.0.1']


# Application definition

INSTALLED_APPS = [
    'accounts',
    'home',
    'widget_tweaks',
    'psycopg2',
    'ckeditor',
    'ckeditor_uploader',
    'debug_toolbar',
    'taggit',
    'taggit_templatetags2',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.postgres'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'tutorial.middleware.LoginRequiredMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    
]

ROOT_URLCONF = 'tutorial.urls'

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
                'django.template.context_processors.media',
                'home.context_processors.blogposts_processor',
               
                
                
            ],
        },
    },
]



WSGI_APPLICATION = 'tutorial.wsgi.application'


#Database
#https://docs.djangoproject.com/en/1.11/ref/settings/#databases

# DATABASES = {
#      'default': {
#          'ENGINE': 'django.db.backends.postgresql_psycopg2',
#          'NAME': 'tutorial',
#          'USER': 'm',
#          : '',
#          'HOST': 'localhost',
#          'PORT': '5432',

 

#      }
#  }

DATABASES = {
    'default': env.db(), # Raises ImproperlyConfigured exception if DATABASE_URL not in os.environ
    
}

DBBACKUP_STORAGE = 'django.core.files.storage.FileSystemStorage'
DBBACKUP_STORAGE_OPTIONS = {'location': os.path.join(BASE_DIR, 'tutorial/backups')}

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH__VALIDATORS = [
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
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')


MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'tutorial/media')

CKEDITOR_UPLOAD_PATH = 'Screenshots/'
CKEDITOR_IMAGE_BACKEND = 'pillow'

CKEDITOR_CONFIGS = {
    'awesome_ckeditor': {
        'toolbar': 'full',
        'height': 300,
        'width': 900,
        
    },
}


LOGIN_URL = '/account/login/'

LOGIN_REDIRECT_URL = '/home/'

LOGIN_EXEMPT_URLS = (
    # r'^home/ajax/blogpostlikes/$',
    r'^account/ajax/validate_username/$',
    r'^account/logout/$',
    r'^account/register/$',
    r'^account/reset-password/$',
    r'^account/reset-password/done/$',
    r'^account/reset-password/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
    r'^account/reset-password/complete/$'

)

EMAIL_HOST = 'localhost'
EMAIL_PORT = 1025

##python -m smtpd -n -c DebuggingServer localhost:1025


