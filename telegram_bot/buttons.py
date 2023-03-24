from telegram import *

from orders.models import Delivery
from orders.utils import get_regions
from telegram_bot.utils import build_menu

BUTTON1_CATEGORIES = "Categories"
BUTTON2_CART = "Cart"
BUTTON3_HELP = "Help"
BUTTON4_ORDERS = "My orders"

regions = get_regions()


def get_base_reply_keyboard():
    keyboard = [
        [KeyboardButton(BUTTON1_CATEGORIES), KeyboardButton(BUTTON2_CART)],
        [KeyboardButton(BUTTON4_ORDERS), KeyboardButton(BUTTON3_HELP)],
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


def regions_reply_markup():
    buttons = [InlineKeyboardButton(text=region.split(' ')[0], callback_data=region) for region in regions.keys()]
    return InlineKeyboardMarkup(build_menu(buttons, n_cols=3))


def cities_reply_markup(region):
    cities = regions[region]
    buttons = [InlineKeyboardButton(text=city, callback_data=city) for city in cities]
    return InlineKeyboardMarkup(build_menu(buttons, n_cols=4))


def deliveries_reply_markup():
    deliveries = Delivery.objects.all().order_by('price')
    buttons = [InlineKeyboardButton(text=f'{d.name} (₴{d.price})', callback_data=f'delivery_{d.id}') for d in deliveries]
    return InlineKeyboardMarkup(build_menu(buttons, n_cols=1))