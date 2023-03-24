import json
import random
import string
from urllib.request import urlopen

from orders.models import Order


def get_regions():
    response = urlopen('https://way-shop-bucket.s3.eu-north-1.amazonaws.com/ua-cities.json')
    data_json = json.loads(response.read())
    y = json.dumps(data_json, ensure_ascii=False).encode('utf8')
    json_str = y.decode()
    data = json.loads(json_str)

    regions = dict()
    for region in data[0]['regions']:
        region_name = region['name']
        for city in region['cities']:
            if region_name not in regions:
                regions[region_name] = list()
                regions[region_name].append(city['name'])
            else:
                regions[region_name].append(city['name'])

    sorted(regions)
    for cities in regions.values():
        cities.sort()

    return regions


def queryset_cities():
    regions = get_regions()
    cities = list()

    i = 0
    for key, value in regions.items():
        lst = list()
        for city in value:
            val = (city, city)
            lst.append(val)
            i += 1
        cities.append((key, lst))

    return cities


def create_unique_id(k=15):
    return ''.join(random.choices(string.digits, k=k))


def unique_order_id():
    order_id = create_unique_id()
    unique = False
    while not unique:
        if not Order.objects.filter(pk=order_id).exists():
            unique = True
        else:
            order_id = create_unique_id()
    return order_id