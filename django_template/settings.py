import django

from django_template.setting_basic import *

DJANGO_ENV = 'DEV_BUG'
print(django.VERSION)
DJANGO_VERSION = str(django.VERSION[0])
if DJANGO_ENV == 'DEV_BUG':
    from django_template.setting_dev_debug import *
elif DJANGO_ENV == 'PROD':
    from django_template.setting_prod import *
