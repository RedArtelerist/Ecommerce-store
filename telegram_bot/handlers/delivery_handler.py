from decimal import Decimal

from telegram import *
from telegram.ext import CallbackContext, ConversationHandler

from coupons.models import Coupon
from orders.models import Delivery
from telegram_bot.buttons import cities_reply_markup, deliveries_reply_markup
from telegram_bot.handlers.cart_handler import get_cart
from telegram_bot.handlers.validators import validate_address
from telegram_bot.utils import debug_requests, build_menu, order_info

CITY, ADDRESS, DELIVERY, CONFIRM = range(10, 14)


@debug_requests
def region_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    region = query.data

    query.edit_message_text(
        text='*Choose your city*',
        reply_markup=cities_reply_markup(region),
        parse_mode=ParseMode.MARKDOWN
    )

    return CITY


@debug_requests
def city_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    city = query.data

    context.user_data['city'] = city

    query.edit_message_text(
        text='❕*Enter your address*',
        parse_mode=ParseMode.MARKDOWN
    )

    return ADDRESS


@debug_requests
def address_handler(update: Update, context: CallbackContext):
    try:
        address = validate_address(update.message.text)
        context.user_data['address'] = address

        update.message.reply_text(
            text='❕*Choose delivery method*',
            reply_markup=deliveries_reply_markup(),
            parse_mode=ParseMode.MARKDOWN
        )

        return DELIVERY
    except Exception as ex:
        update.message.reply_text(f'❗️ {str(ex)}')
        return ADDRESS


@debug_requests
def delivery_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    delivery_id = int(query.data.split('_')[1])
    context.user_data['delivery'] = int(delivery_id)

    cart = get_cart(query.message.chat_id)
    cart_text, total_price = order_info(cart)
    context.user_data['total_price'] = total_price
    discount_info = ''

    if 'coupon' in context.user_data:
        try:
            coupon = Coupon.objects.get(pk=context.user_data['coupon'])
            discount = round((coupon.discount / Decimal('100')) * total_price)
            context.user_data['discount'] = coupon.discount
            context.user_data['discount_price'] = discount
            total_price -= discount
            discount_info = f'<b>Discount:</b> <code>-{coupon.discount}%(-₴{discount})</code>\n'
        except: pass
    else:
        context.user_data['discount'] = 0
        context.user_data['discount_price'] = 0

    delivery = Delivery.objects.filter(pk=context.user_data['delivery']).first()

    if delivery is None:
        query.answer('Something went wrong')
        return ConversationHandler.END

    grand_price = total_price + delivery.price
    context.user_data['delivery_price'] = delivery.price

    cart_info = f'<pre>Your order:</pre>\n{cart_text}\n{discount_info}<b>Delivery:</b> <code>₴{delivery.price}</code>\n' \
                f'<b>Grand total:</b> <code>₴{grand_price}</code>\n'

    personal_info = f'<pre>Your personal info:</pre>\n' \
                    f'<b>First name:</b> <i>{context.user_data["customer_first_name"]}</i>\n' \
                    f'<b>Last name:</b> <i>{context.user_data["customer_last_name"]}</i>\n' \
                    f'<b>Email:</b> <i>{context.user_data["customer_email"]}</i>\n' \
                    f'<b>Phone:</b> <i>{context.user_data["phone"]}</i>\n'

    recipient_info = f'<pre>Recipient info:</pre>\n' \
                     f'<b>First name:</b> <i>{context.user_data["recipient_first_name"]}</i>\n' \
                     f'<b>Last name:</b> <i>{context.user_data["recipient_last_name"]}</i>\n' \
                     f'<b>Email:</b> <i>{context.user_data["recipient_email"]}</i>\n'

    address_info = f'<pre>Address:</pre>\n<i>{context.user_data["city"]}, {context.user_data["address"]}</i>'

    total_info = f'{cart_info}\n{personal_info}\n{recipient_info}\n{address_info}'

    button_list = [
        InlineKeyboardButton(text='Yes', callback_data='confirm_yes'),
        InlineKeyboardButton(text='No', callback_data='confirm_no'),
    ]
    reply_markup = InlineKeyboardMarkup(build_menu(button_list, n_cols=2))
    query.edit_message_text(
        text=f'{total_info}\n\n<b>Confirm entered information?</b>',
        reply_markup=reply_markup, parse_mode=ParseMode.HTML
    )

    return CONFIRM