#
# www_app
#
# Returns the first directory name of the request full path.
# Used to split the root app url destination.
#
from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter(name='www_app')
@stringfilter
def www_app(value):
    """
    Returns the first directory name of the request full path.
    Used to split the root app url destination.

    :param value: string
    :returns string
    """
    try:
        url_parts = value.split('/')
        url_app = '/{!s}'.format(url_parts[1])

    except IndexError:
        url_app = ''

    return url_app
