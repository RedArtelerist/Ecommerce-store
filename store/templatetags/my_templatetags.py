from django import template
from store.models import *

register = template.Library()


@register.simple_tag
def get_products(company):
    return Product.objects.filter(company=company).order_by('-sales')


@register.simple_tag
def relative_url(value, field_name, urlencode=None):
    url = '?{}={}'.format(field_name, value)
    if urlencode:
        querystring = urlencode.split('&')
        filtered_querystring = filter(lambda p: p.split('=')[0] != field_name, querystring)
        encoded_querystring = '&'.join(filtered_querystring)
        url = '{}&{}'.format(url, encoded_querystring)
    return url


@register.filter
def user_in(objects, user):
    if user.is_authenticated:
        return objects.filter(user=user).exists()
    return False