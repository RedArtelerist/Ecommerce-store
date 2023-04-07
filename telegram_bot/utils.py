import functools
import logging
import random
import string

from django.conf import settings

from cart.models import UserCart
from store.models import Product


def logger_factory(logger):
    def debug_requests(f):

        @functools.wraps(f)
        def inner(*args, **kwargs):

            try:
                logger.debug('Обращение в функцию `{}`'.format(f.__name__))
                return f(*args, **kwargs)
            except Exception as e:
                logger.exception('Ошибка в функции `{}`'.format(f.__name__))
                raise

        return inner

    return debug_requests


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)
debug_requests = logger_factory(logger=logger)


def build_menu(buttons, n_cols, header_buttons=None, footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, header_buttons)
    if footer_buttons:
        menu.append(footer_buttons)
    return menu


def order_info(cart: UserCart):
    items_cart = dict(cart.items_cart)
    cart_items = []
    total_price = 0
    for prod_id, item in items_cart.items():
        product = Product.objects.filter(pk=prod_id).first()
        if product is None:
            continue

        price = int(item['price'])
        quantity = item['quantity']
        cart_items.append(f'<b>{product.name}</b>:\n<code>₴{price} x {quantity} — ₴{price * quantity}</code>\n')
        total_price += price * quantity

    if len(cart_items) == 0:
        cart_text = '⚠️<b>Your cart is empty</b>'
    else:
        cart_text = '\n'.join(cart_items)
        cart_text += f'\n<b>Total:</b> <code>₴{total_price}</code>'

    return cart_text, total_price


def unique_code(n: int):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=n))


def get_line_items(cart: UserCart, delivery_price: int):
    line_items = []
    items_cart = dict(cart.items_cart)
    for prod_id, data in items_cart.items():
        product = Product.objects.filter(id=prod_id).first()

        line_items.append({
                "price_data": {
                    "currency": "uah",
                    "product_data": {
                        "name": product.name,
                        "images": [product.imageURL],
                    },
                    "unit_amount": int(data['price'])*100,
                },
                "quantity": data['quantity'],
            }
        )

    line_items.append(
        {
            "price_data": {
                "currency": "uah",
                "product_data": {
                    "name": "Delivery",
                },
                "unit_amount": delivery_price * 100,
            },
            "quantity": 1,
        }
    )

    return line_items


def get_current_site():
    debug = settings.DEBUG
    if debug:
        return 'http://127.0.0.1:8000/'
    else:
        return f'{settings.TELEGRAM_WEBHOOK_URL}/'