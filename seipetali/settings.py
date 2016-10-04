# -*- coding: utf-8 -*-

"""
Django settings for seipetali project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""



# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from platform import node

BASE_DIR = os.path.dirname(os.path.dirname(__file__))



DEVELOPMENT_HOST = ['spidermonkey.lan','spidermonkey','spidermonkey.local','tyrell.lan','tyrell.local','tyrell.metalabs.org','kingkong.lan','vagrant-ubuntu-trusty-32']
PRODUCTION_HOST = ['ip-10-33-185-58','ip-10-107-22-82','ip-10-104-36-106']


ADMINS = (
    ('elfo', 'paolo@digitalmonkeys.it'),
    # ('Your Name', 'your_email@example.com'),
)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'g5f%qb2$df2ky8t)ei#=*--5ic3$irqot^#d%evrv0p%*4ln69'

# SECURITY WARNING: don't run with debug turned on in production!
TEST_PRODUCTION = False

if node() in PRODUCTION_HOST or TEST_PRODUCTION:
    DEBUG = False
    DB_DEBUG = False
elif node() in DEVELOPMENT_HOST:
    DEBUG = True
    DB_DEBUG = True
    TEMPLATE_DEBUG = True
else:
    raise Exception("Cannot determine execution mode for host '%s'.  Please check DEVELOPMENT_HOST and PRODUCTION_HOST in settings_local.py." % node())




ALLOWED_HOSTS = ['.iseipetali.it']

APPEND_SLASH = True

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',


    # seipetali apps
    'common',
    'seipetali',
    'user',
    'alloggio',
    'seipetali_configuration',
    'address',
    'faq',
    'reservation',
    'dataqrcode',
    'notification'

    # 'python-phonenumbers'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'seipetali.urls'

WSGI_APPLICATION = 'seipetali.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases


if DB_DEBUG:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }
else:
    DATABASES = {
        'default': {
                    'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
                    'NAME': 'seipetali_prod',                      # Or path to database file if using sqlite3.
                    # 'NAME': 'manabu_prod',                      # Or path to database file if using sqlite3.
                    # The following settings are not used with sqlite3:
                    'USER': 'seipetali_prod',
                    'PASSWORD': 'DvoGS9W1jEDhdTD',
                    'HOST': 'localhost',                      # Empty for localhost through domain sockets or           '127.0.0.1' for localhost through TCP.
                    'PORT': '',                      # Set to empty string for default.
            }
    }

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/


LANGUAGE_CODE = 'it'

# _ = lambda s: s
from django.utils.translation import ugettext_lazy as _

LANGUAGES = (
    ('it', _('Italian')),
    ('en', _('English')),
)

# LANGUAGE_COOKIE_NAME = 'seipetali_language'

LOCALE_PATHS = (
    os.path.join(BASE_DIR, "locale"),
)



TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'


TEMPLATE_DIRS = (os.path.join(os.path.dirname(__file__), '..', 'templates').replace('\\','/'),)




# Configurazione modulo site


INSTALLED_APPS += (

    # 'avatar',
    'django.contrib.sites',
)

SITE_ID  = 1




# Configurazione base  TEMPLATE_CONTEXT_PROCESSORS
# TEMPLATE CONFIGURATION

from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS as TCP
TEMPLATE_CONTEXT_PROCESSORS = TCP + (
    'django.core.context_processors.i18n',
    'django.core.context_processors.request',
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    'django.core.context_processors.request',
)




# Configurazione delle classe utenti e profili'

AUTH_PROFILE_MODULE = 'user.UserProfile'
AUTH_USER_MODEL = 'user.User'
# AUTH_USER_MODEL = 'auth.User'
AUTHENTICATION_BACKENDS = ()




###########################################
# Configurazione del modulo django-allauth

TEMPLATE_CONTEXT_PROCESSORS += (
    "allauth.account.context_processors.account",
    "allauth.socialaccount.context_processors.socialaccount",
)


AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    "django.contrib.auth.backends.ModelBackend",
    # `allauth` specific authentication methods, such as login by e-mail
    "allauth.account.auth_backends.AuthenticationBackend",
)



INSTALLED_APPS += (

    # 'avatar',
    'allauth',
    'allauth.account',
    # 'allauth.socialaccount',
    # ... include the providers you want to enable:
    # 'allauth.socialaccount.providers.dropbox',
    # 'allauth.socialaccount.providers.facebook',
    # 'allauth.socialaccount.providers.google',
    # 'allauth.socialaccount.providers.github',
    # 'allauth.socialaccount.providers.linkedin',
    # 'allauth.socialaccount.providers.openid',
    # 'allauth.socialaccount.providers.persona',
    # 'allauth.socialaccount.providers.soundcloud',
    # 'allauth.socialaccount.providers.stackexchange',
    # 'allauth.socialaccount.providers.twitch',
    # 'allauth.socialaccount.providers.twitter',
    # 'allauth.socialaccount.providers.vimeo',
    # 'allauth.socialaccount.providers.weibo',
)




# Available settings:
#

LOGIN_REDIRECT_URL = "/"

ACCOUNT_ADAPTER = "allauth.account.adapter.DefaultAccountAdapter"
# ACCOUNT_ADAPTER = 'users.accountadapter.AccountAdapter'

# ACCOUNT_ADAPTER (="allauth.account.adapter.DefaultAccountAdapter")
# Specifies the adapter class to use, allowing you to alter certain default behaviour.

# ACCOUNT_AUTHENTICATION_METHOD (="username" | "email" | "username_email")
ACCOUNT_AUTHENTICATION_METHOD = "username_email"
# Specifies the login method to use -- whether the user logs in by entering his username, e-mail address, or either one of both.



# ACCOUNT_EMAIL_CONFIRMATION_ANONYMOUS_REDIRECT_URL (=settings.LOGIN_URL)
# The URL to redirect to after a successful e-mail confirmation, in case no user is logged in.

# ACCOUNT_EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_URL (=None)
# The URL to redirect to after a successful e-mail confirmation, in case of an authenticated user. Set to None to use settings.LOGIN_REDIRECT_URL.

# ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS (=3)
# Determines the expiration date of email confirmation mails (# of days).

ACCOUNT_EMAIL_REQUIRED = True
# ACCOUNT_EMAIL_REQUIRED (=False)
# The user is required to hand over an e-mail address when signing up.

if DEBUG:
    ACCOUNT_EMAIL_VERIFICATION = "optional"
else:
    ACCOUNT_EMAIL_VERIFICATION = "mandatory"

# ACCOUNT_EMAIL_VERIFICATION = "mandatory"

# ACCOUNT_EMAIL_VERIFICATION (="mandatory" | "optional" | "none")
# Determines the e-mail verification method during signup. When set to "mandatory" the user is blocked from logging in until the email address is verified. Choose "optional" or "none" to allow logins with an unverified e-mail address. In case of "optional", the e-mail verification mail is still sent, whereas in case of "none" no e-mail verification mails are sent.

ACCOUNT_EMAIL_SUBJECT_PREFIX = u'✻ 6 Petali - '
# ACCOUNT_EMAIL_SUBJECT_PREFIX (="[Site] ")
# Subject-line prefix to use for email messages sent. By default, the name of the current Site (django.contrib.sites) is used.



# Esegue il logout senza chedere conferma
ACCOUNT_LOGOUT_ON_GET = True
# ACCOUNT_LOGOUT_ON_GET (=False)
# Determines whether or not the user is automatically logged out by a mere GET request. See documentation for the LogoutView for details.

ACCOUNT_LOGOUT_REDIRECT_URL = "/"
# The URL (or URL name) to return to after the user logs out. This is the counterpart to Django's LOGIN_REDIRECT_URL.

# ACCOUNT_SIGNUP_FORM_CLASS (=None)
# A string pointing to a custom form class (e.g. 'myapp.forms.SignupForm') that is used during signup to ask the user for additional input (e.g. newsletter signup, birth date). This class should implement a 'save' method, accepting the newly signed up user as its only parameter.

# ACCOUNT_SIGNUP_PASSWORD_VERIFICATION (=True)
# When signing up, let the user type in his password twice to avoid typ-o's.

# ACCOUNT_UNIQUE_EMAIL (=True)
# Enforce uniqueness of e-mail addresses.

# ACCOUNT_USER_MODEL_USERNAME_FIELD = "email"
# ACCOUNT_USER_MODEL_USERNAME_FIELD (="username")
# The name of the field containing the username, if any. See custom user models.

# ACCOUNT_USER_MODEL_EMAIL_FIELD (="email")
# The name of the field containing the email, if any. See custom user models.


# ACCOUNT_USER_DISPLAY = 'users.utils.user_display'
# ACCOUNT_USER_DISPLAY (=a callable returning user.username)
# A callable (or string of the form 'some.module.callable_name') that takes a user as its only argument and returns the display name of the user. The default implementation returns user.username.

# ACCOUNT_USERNAME_MIN_LENGTH (=1)
# An integer specifying the minimum allowed length of a username.

# ACCOUNT_USERNAME_BLACKLIST (=[])
# A list of usernames that can't be used by user.

ACCOUNT_USERNAME_REQUIRED = False
# ACCOUNT_USERNAME_REQUIRED (=True)
# The user is required to enter a username when signing up. Note that the user will be asked to do so even if ACCOUNT_AUTHENTICATION_METHOD is set to email. Set to False when you do not wish to prompt the user to enter a username.

# ACCOUNT_PASSWORD_INPUT_RENDER_VALUE (=False)
# render_value parameter as passed to PasswordInput fields.

# ACCOUNT_PASSWORD_MIN_LENGTH (=6)
# An integer specifying the minimum password length.

# SOCIALACCOUNT_ADAPTER = 'users.adapter.MySocialAccountAdapter'

# Aggiunto per il modulo invitation
# SOCIALACCOUNT_ADAPTER ="users.accountadapter.SocialAccountAdapter"
# SOCIALACCOUNT_ADAPTER (="allauth.socialaccount.adapter.DefaultSocialAccountAdapter")
# Specifies the adapter class to use, allowing you to alter certain default behaviour.

# SOCIALACCOUNT_QUERY_EMAIL (=ACCOUNT_EMAIL_REQUIRED)
# Request e-mail address from 3rd party account provider? E.g. using OpenID AX, or the Facebook "email" permission.

SOCIALACCOUNT_QUERY_EMAIL = True

SOCIALACCOUNT_AUTO_SIGNUP = True
# SOCIALACCOUNT_AUTO_SIGNUP (=True)
# Attempt to bypass the signup form by using fields (e.g. username, email) retrieved from the social account provider. If a conflict arises due to a duplicate e-mail address the signup form will still kick in.

AVATAR_SUPPORT = 'avatar'
SOCIALACCOUNT_AVATAR_SUPPORT = 'avatar'
# SOCIALACCOUNT_AVATAR_SUPPORT (= 'avatar' in settings.INSTALLED_APPS)
# Enable support for django-avatar. When enabled, the profile image of the user is copied locally into django-avatar at signup.

# SOCIALACCOUNT_PROVIDERS (= dict)
# Dictionary containing provider specific settings.

SOCIALACCOUNT_EMAIL_REQUIRED = True
SOCIALACCOUNT_EMAIL_VERIFICATION = False

SOCIALACCOUNT_ENABLED = True

SESSION_SERIALIZER='django.contrib.sessions.serializers.PickleSerializer'

# SESSION_ENGINE='common.session_backend'

SOCIALACCOUNT_PROVIDERS = \
    {
        # 'google':
        # { 'SCOPE': [
        #         'https://www.googleapis.com/auth/userinfo.profile'
        #         ,'https://www.googleapis.com/auth/userinfo.email'
        #         # ,'https://www.googleapis.com/auth/plus.login'
        #         # ,'https://www.googleapis.com/auth/plus.me'
        #     ],
        #   'AUTH_PARAMS': { 'access_type': 'online' } },
        #
        # 'facebook':
        # { 'SCOPE': [
        #         'email'
        #         ,'publish_stream'
        #     ],
        #   'AUTH_PARAMS': { 'auth_type': 'reauthenticate' },
        #   'METHOD': 'oauth2' ,
        #   'LOCALE_FUNC': lambda request: 'it_IT'}

    }






################################
######### EMAIL CONFIGURATION SETTING ########
ALWAYS_SEND_EMAIL = True
if DEBUG and not ALWAYS_SEND_EMAIL:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
else:
    #Email
    # EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_BACKEND = 'common.email_backends.EmailBackend'
    # EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

    DEFAULT_FROM_EMAIL = '6 petali <web@iseipetali.it>'
    SERVER_EMAIL = 'web@iseipetali.it'

    EMAIL_USE_TLS = True
    EMAIL_HOST_USER = 'web@iseipetali.it'
    EMAIL_PORT = 587
    EMAIL_HOST = 'smtp-out.kpnqwest.it'
    EMAIL_HOST_PASSWORD = '!6P3_tali'





############################





####################################
################ PHOTOLOGUE CONF  ####################
INSTALLED_APPS += (
    'photologue',
    'sortedm2m',
)



###################################
######## STATIC CONF

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = 'static'

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(os.path.dirname(__file__),'static').replace('\\','/'),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # other finders..
    'compressor.finders.CompressorFinder',
)



############ MEDIA CONF

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')



# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = "/media/"



####################################
################ Compressor CONF  ####################
INSTALLED_APPS += (
    'compressor',

)
COMPRESS_ENABLED = False
COMPRESS_OFFLINE = True


####################################
################ crispy_forms CONF  ####################
INSTALLED_APPS += (
    'crispy_forms',
)

CRISPY_TEMPLATE_PACK = 'bootstrap3'




############ TASTYPIE
TASTYPIE_ENABLED = True



if TASTYPIE_ENABLED:

    # DJANGO CELERY
    INSTALLED_APPS += (
        'tastypie',
    )


    # TASTYPIE_DATETIME_FORMATTING = 'rfc-2822'
    # TASTYPIE_DATETIME_FORMATTING='iso-8601'

TASTYPIE_DEFAULT_FORMATS = ['json']

TASTYPIE_SWAGGER_ENABLED = True



if TASTYPIE_SWAGGER_ENABLED:
    INSTALLED_APPS += (
        'tastypie_swagger',
    )

    TASTYPIE_SWAGGER_API_MODULE = 'seipetali.urls_api.v1_api'
    TASTYPIE_DATETIME_FORMATTING = 'rfc-2822'
    TASTYPIE_DATETIME_FORMATTING='iso-8601'



# DJANGO ANGULAR
INSTALLED_APPS += (
    'djangular',
)




#CONFIG MODELTRANSLATION

INSTALLED_APPS += (
    'modeltranslation',
)



MODELTRANSLATION_DEFAULT_LANGUAGE = 'it'

MODELTRANSLATION_FALLBACK_LANGUAGES = ('it', 'en')




#CONFIG https://github.com/llazzaro/django-scheduler
INSTALLED_APPS += (
    'schedule',
)

TEMPLATE_CONTEXT_PROCESSORS += ("django.core.context_processors.request",)








#### CONFIGURATION DJANGO CMS

INSTALLED_APPS += (

    'cms',  # django CMS itself
    'mptt',  # utilities for implementing a tree
    'menus',  # helper for model independent hierarchical website navigation
    'sekizai',  # for javascript and css management
    'djangocms_admin_style',  # for the admin skin. You **must** add 'djangocms_admin_style' in the list **before** 'django.contrib.admin'.
    'reversion',

    # 'treebeard',

    'easy_thumbnails',
    'filer',
    'djangocms_text_ckeditor',
    # 'djangocms_picture',
    'cmsplugin_filer_file',
    'cmsplugin_filer_folder',
    'cmsplugin_filer_link',
    'cmsplugin_filer_image',
    'cmsplugin_filer_teaser',
    'cmsplugin_filer_video',
)
MIGRATION_MODULES = {
    'cms': 'cms.migrations_django',
    'menus': 'menus.migrations_django',
    'djangocms_text_ckeditor': 'djangocms_text_ckeditor.migrations_django',
    # 'djangocms_picture': 'djangocms_picture.migrations_django',
    'filer': 'filer.migrations_django',
    'cmsplugin_filer_file': 'cmsplugin_filer_file.migrations_django',
    'cmsplugin_filer_link': 'cmsplugin_filer_link.migrations_django',
    'cmsplugin_filer_folder': 'cmsplugin_filer_folder.migrations_django',
    'cmsplugin_filer_image': 'cmsplugin_filer_image.migrations_django',
    'cmsplugin_filer_teaser': 'cmsplugin_filer_teaser.migrations_django',
    'cmsplugin_filer_video': 'cmsplugin_filer_video.migrations_django',
}

TEMPLATE_CONTEXT_PROCESSORS += (
    'sekizai.context_processors.sekizai',
    'cms.context_processors.cms_settings',
)

TEXT_SAVE_IMAGE_FUNCTION='cmsplugin_filer_image.integrations.ckeditor.create_image_plugin'

MIDDLEWARE_CLASSES += (

    'cms.middleware.user.CurrentUserMiddleware',
    'cms.middleware.page.CurrentPageMiddleware',
    # 'cms.middleware.toolbar.ToolbarMiddleware',
    'common.cms_middleware.CustomToolbarMiddleware',
    'cms.middleware.language.LanguageCookieMiddleware',
)

CMS_TEMPLATES = (
    ('cms/template_1.html', 'Template One'),
    ('cms/2col-3-9.html', 'Panel left + Main'),
    # ('template_2.html', 'Template Two'),
)
CMS_TOOLBARS = [
    # CMS Toolbars
    'cms.cms_toolbar.PlaceholderToolbar',
    'cms.cms_toolbar.PageToolbar',
    'common.cms_toolbar.CustomToolbar',

    # 3rd Party Toolbar
    # 'aldryn_blog.cms_toolbar.BlogToolbar',
]

TEXT_ADDITIONAL_TAGS = ('iframe',)
TEXT_ADDITIONAL_ATTRIBUTES = ('scrolling', 'allowfullscreen', 'frameborder')

CMS_PERMISSION = True
# CKEDITOR_SETTINGS = {
#     'language': '{{ language }}',
#     'toolbar': 'CMS',
#     'skin': 'moono',
# }
CKEDITOR_SETTINGS = {
    'language': '{{ language }}',
    'toolbar_HTMLField': [
        ['Undo', 'Redo'],
        ['ShowBlocks'],
        ['Format', 'Styles'],

    ],

    'toolbar_CMS': [
                                ['Undo', 'Redo'],
                                ['cmsplugins', '-', 'ShowBlocks'],
                                ['Format', 'Styles'],
                                ['TextColor', 'BGColor', '-', 'PasteText', 'PasteFromWord'],
                                ['Maximize', ''],
                                '/',
                                ['Bold', 'Italic', 'Underline', '-', 'Subscript', 'Superscript', '-', 'RemoveFormat'],
                                ['JustifyLeft', 'JustifyCenter', 'JustifyRight'],
                                ['HorizontalRule'],
                                ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'Table'],
                                ['Source'],
                                ['Flash', 'Table', 'HorizontalRule', 'Smiley', 'SpecialChar', 'PageBreak', 'Iframe' ]
                        ],
    'skin': 'moono',
}
CKEDITOR_UPLOAD_PATH = "uploads/"


THUMBNAIL_HIGH_RESOLUTION = True

THUMBNAIL_PROCESSORS = (
    'easy_thumbnails.processors.colorspace',
    'easy_thumbnails.processors.autocrop',
    'easy_thumbnails.processors.scale_and_crop',
    'filer.thumbnail_processors.scale_and_crop_with_subject_location',
    'easy_thumbnails.processors.filters',
)


# DEBUG TOOLBAR

INSTALLED_APPS += (
    # 'debug_toolbar',
)

MIDDLEWARE_CLASSES += (
    # ...
    # 'debug_toolbar.middleware.DebugToolbarMiddleware',
    'debug_panel.middleware.DebugPanelMiddleware',
    # ...
)




INSTALLED_APPS += (
    'django_migration_fixture',
)


# FIXTURE_DIRS = (
#    '/path/to/myapp/fixtures/',
    # os.path.join(BASE_DIR, 'user/fixtures'),
# )



# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
        'verbose': {
            'format': '%(asctime)s [%(levelname)s] %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '[%(levelname)s] %(message)s'
        },
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'formatter': 'verbose',
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'console':{
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'standard'
        },
        'default': {
            'level':'ERROR',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': 'logs/mylog.log',
            'maxBytes': 1024*1024*5, # 5 MB
            'backupCount': 5,
            'formatter':'standard',
            },
        },
    'loggers': {
        '': {
            'handlers': ['default','mail_admins','console'],
            'level': 'INFO',
            'propagate': True
        },
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}







SHOW_HOME_ALWAYS = False
PHOTOLOGUE_FORCE_JPEG = True


SEIPETALI_ADMINS = (
    ('elfo', 'paolo@digitalmonkeys.it'),
#    ('info', 'info@iseipetali.it'),
    ('iseipetali', 'iseipetali@iseipetali.it'),
    ('Maurizio', 'maurizio.zambelli@adcoop.it'),
)


SEIPETALI_SEARCH_ENABLED = True


if DEBUG:
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
        }
    }
