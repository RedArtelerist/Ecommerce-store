from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from telegram.ext import CallbackContext
from telegram_bot.utils import debug_requests
from cart.models import UserCart
from store.models import Product
from telegram_bot.utils import build_menu, logger, order_info


def get_cart(chat_id):
    cart = UserCart.objects.filter(chat_id=chat_id).first()

    if cart is None:
        cart = UserCart(chat_id=chat_id, items_cart=[], coupon=0, items_wishlist=[])
        cart.save()

    return cart


def show_cart(update: Update, context: CallbackContext, chat_id, message_id, edit: bool):
    cart = get_cart(chat_id)
    cart_text, total = order_info(cart)

    if total == 0:
        if edit:
            update.callback_query.edit_message_text(cart_text, parse_mode=ParseMode.HTML)
        else:
            update.message.reply_text(cart_text, parse_mode=ParseMode.HTML)
    else:
        button_list = [
            InlineKeyboardButton(text='Edit cart', callback_data='edit_cart'),
            InlineKeyboardButton(text='Clear cart', callback_data='clear_cart'),
            InlineKeyboardButton(text='Close', callback_data='close_cart'),
            InlineKeyboardButton(text='Order', callback_data='checkout_start')
        ]

        reply_markup = InlineKeyboardMarkup(build_menu(button_list, n_cols=2))
        if edit:
            update.callback_query.edit_message_text(cart_text, reply_markup=reply_markup, parse_mode=ParseMode.HTML)
        else:
            update.message.reply_text(cart_text, reply_markup=reply_markup, parse_mode=ParseMode.HTML)

            if cart.message_id != -1:
                try:
                    context.bot.delete_message(chat_id=chat_id, message_id=cart.message_id)
                except: pass

            cart.message_id = message_id + 1
            cart.save()


def add_to_cart(update: Update, prod_id, context: CallbackContext):
    query = update.callback_query
    chat_id = query.message.chat_id

    try:
        product = Product.objects.get(pk=prod_id)
        cart = get_cart(chat_id)
        cart_items = dict(cart.items_cart)
        product_id = str(prod_id)

        if product_id in cart_items:
            if cart_items[product_id]['quantity'] == 5:
                query.answer(text='You can add a maximum of 5 items per product')
            else:
                cart_items[product_id]['quantity'] += 1
        else:
            logger.info(product.discount_price)
            cart_items[product_id] = {
                'quantity': 1,
                'price': str(product.discount_price)
            }
        cart.items_cart = cart_items.items()
        cart.save()
        query.answer('Product was successfully added')
    except Exception:
        query.answer('Product not found')


def remove_from_cart(update: Update, prod_id, context: CallbackContext, full=False):
    query = update.callback_query
    chat_id = query.message.chat_id

    try:
        cart = get_cart(chat_id)
        cart_items = dict(cart.items_cart)
        product_id = str(prod_id)

        cart_items[product_id]['quantity'] -= 1
        if cart_items[product_id]['quantity'] == 0 or full:
            cart_items.pop(product_id, None)

        cart.items_cart = cart_items.items()
        cart.save()
    except Exception:
        query.answer('Something went wrong')


def clear_cart(update: Update, context: CallbackContext):
    query = update.callback_query
    chat_id = query.message.chat_id

    cart = get_cart(chat_id)

    cart.items_cart = []
    cart.save()
    query.delete_message()


@debug_requests
def get_cart_handler(update: Update, context: CallbackContext, edit=False):
    if edit:
        chat_id = update.callback_query.message.chat_id
        message_id = update.callback_query.message.message_id
    else:
        chat_id = update.message.chat_id
        message_id = update.message.message_id
        update.message.delete()

    show_cart(update, context, chat_id, message_id, edit)


@debug_requests
def clear_cart_handler(update: Update, context: CallbackContext):
    clear_cart(update, context)


@debug_requests
def close_cart_handler(update: Update, context: CallbackContext):
    chat_id = update.callback_query.message.chat_id
    cart = get_cart(chat_id)

    try:
        context.bot.delete_message(chat_id=chat_id, message_id=cart.message_id)
    except: pass


@debug_requests
def edit_cart_handler(update: Update, context: CallbackContext):
    chat_id = update.callback_query.message.chat_id
    cart = dict(get_cart(chat_id).items_cart)

    buttons = []
    for prod_id, item in cart.items():
        product = Product.objects.filter(pk=prod_id).first()
        if product is None:
            continue
        else:
            buttons.append([InlineKeyboardButton(text=f'{product.name} x{item["quantity"]}', callback_data=f'empty_{prod_id}')])
            buttons.append(
                [
                    InlineKeyboardButton(text='➕', callback_data=f'plus_{prod_id}'),
                    InlineKeyboardButton(text='➖', callback_data=f'minus_{prod_id}'),
                    InlineKeyboardButton(text='✖️', callback_data=f'remove_{prod_id}'),
                ]
            )
    buttons.append([InlineKeyboardButton(text='Back ⬅️', callback_data='back_cart')])
    update.callback_query.edit_message_text('Your cart:', reply_markup=InlineKeyboardMarkup(buttons), parse_mode=ParseMode.MARKDOWN)