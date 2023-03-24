from telegram import *
from telegram.ext import *

from store.models import Category, Product
from telegram_bot.utils import *


def get_categories_buttons():
    categories = Category.objects.filter(parent__isnull=True)
    button_list = []
    for item in categories:
        button_list.append(InlineKeyboardButton(text=item.name, callback_data=f"category_{item.id}"))

    reply_markup = InlineKeyboardMarkup(build_menu(button_list, n_cols=2))
    return reply_markup


@debug_requests
def categories_handler(update: Update, context: CallbackContext):
    try:
        chat_id = update.message.chat_id
        update.message.delete()
        context.bot.delete_message(chat_id=chat_id, message_id=context.user_data['last_menu_msg'])
    except: pass

    update.message.reply_text('All categories:', reply_markup=get_categories_buttons())
    context.user_data['last_menu_msg'] = update.message.message_id + 1


@debug_requests
def subcategories_handler(update: Update, id: int, context: CallbackContext):
    query = update.callback_query
    category = Category.objects.get(pk=id)
    subcategories = Category.objects.filter(parent=category).order_by('name')

    button_list = []
    for item in subcategories:
        button_list.append(InlineKeyboardButton(text=item.name, callback_data=f"subcategory_{item.id}"))

    button_list.append(InlineKeyboardButton(text='Back ⬅️', callback_data='back_menu'))

    reply_markup = InlineKeyboardMarkup(build_menu(button_list, n_cols=1))
    query.edit_message_text(f'Subcategories for category <i>{category.name}</i>:', reply_markup=reply_markup, parse_mode=ParseMode.HTML)


@debug_requests
def products_handler(update: Update, id: int, context: CallbackContext, status=True):
    query = update.callback_query
    category = Category.objects.get(pk=id)
    products = Product.objects.filter(category=category, available=True).order_by('name')

    button_list = []
    for item in products:
        button_list.append(InlineKeyboardButton(text=item.name, callback_data=f"product_{item.id}"))

    button_list.append(InlineKeyboardButton(text='Back ⬅️', callback_data=f'back_category:{category.parent.id}'))

    reply_markup = InlineKeyboardMarkup(build_menu(button_list, n_cols=1))
    if status:
        query.edit_message_text(f'All available products in <i>{category.name}</i>:', reply_markup=reply_markup, parse_mode=ParseMode.HTML)
    else:
        query.delete_message()
        query.message.reply_text(f'All available products in <i>{category.name}</i>:', reply_markup=reply_markup, parse_mode=ParseMode.HTML)


@debug_requests
def product_detail_handler(update: Update, id: int, context: CallbackContext):
    query = update.callback_query
    product = Product.objects.get(pk=id)

    detail = f'<b>{product.name}</b>\n\n<b>Specs:</b>\n<i>{product.shortSpecifications}</i>\n\n'
    price = f'<code>₴{product.discount_price}</code>'
    if product.discount:
        price = f'<s>₴{product.price}</s> {price}'

    caption = detail + f'<b>Price:</b> {price}'
    photo_url = product.imageURL

    button_list = [
        InlineKeyboardButton(text='Add to cart', callback_data=f'add_{product.id}'),
        InlineKeyboardButton(text='View on site', url=f'http://127.0.0.1:8000/{product.id}/{product.slug}/'),
        InlineKeyboardButton(text='Back ⬅️', callback_data=f'back_subcategory:{product.category.id}')
    ]
    reply_markup = InlineKeyboardMarkup(build_menu(button_list, n_cols=2))

    query.delete_message()
    query.message.reply_photo(photo=photo_url, caption=caption, reply_markup=reply_markup, parse_mode=ParseMode.HTML)