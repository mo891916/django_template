import os
from django_template.setting_basic import BASE_DIR

DEBUG = False

# -- add --
import logging
import django.utils.log
import logging.handlers

# -- modify --
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format': '%(asctime)s %(levelname)s %(pathname)s %(filename)s %(module)s %(funcName)s %(lineno)d: %(message)s'
        },
        'simple': {
            'format': '%(asctime)s %(levelname)s : %(message)s'
        },
        # 日志格式
    },
    'filters': {
    },
    'handlers': {
        'default': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'log/all.log',  # 日志输出文件
            'maxBytes': 50000 * 1024,
            'backupCount': 20,
            'formatter': 'simple',
        },
        'request_handler': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'log/request.log',
            'maxBytes': 50000 * 1024,
            'backupCount': 20,
            'formatter': 'simple',
        },
        'error': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'log/error.log',
            'maxBytes': 50000 * 1024,
            'backupCount': 20,
            'formatter': 'standard',
        },
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'mydb': {
            'level': 'DEBUG',
            'class': 'apps.user.handlers.DatabaseHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'default', 'mydb'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
            'propagate': True
        },
        'django.security.DisallowedHost': {
            'handlers': ['error', 'mydb'],
            'propagate': False,
        },
        'django.request': {
            'handlers': ['error'],
            'level': 'WARN',
            'propagate': False
        },
        'django.print': {
            'handlers': ['console', 'error'],
            'level': 'DEBUG',
            'propagate': False
        },
        'log_request': {
            'handlers': ['request_handler'],
            'level': 'DEBUG'
        }
    }
}

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'django',
        'USER': 'django',
        'PASSWORD': 'django_template',
        'HOST': '192.168.1.35',
        'PORT': '9306',
    },
}

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "collectedstatic")

SESSION_SAVE_EVERY_REQUEST = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_COOKIE_AGE = 7200
