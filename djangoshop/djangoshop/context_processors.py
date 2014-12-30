# See
# http://blog.khmelyuk.com/2011/10/django-use-global-variables-on.html
# http://chriskief.com/2013/09/19/access-django-constants-from-settings-py-in-a-template/

from django.conf import settings


def global_settings(request):
    return {
        'PRODUCTS_IMG_DIR': settings.PRODUCTS_IMG_DIR
    }