from telegram import *
from telegram.ext import *

from store.models import Category, Product, Review
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

    button_list.append(InlineKeyboardButton(text='Back ⬅️', callback_data=f'category_{category.parent.id}'))

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
    rate = f'⭐️: {product.rate}/5\n'
    if product.discount:
        price = f'<s>₴{product.price}</s> {price}'

    caption = detail + rate + f'<b>Price:</b> {price}'
    photo_url = product.imageURL

    button_list = [
        InlineKeyboardButton(text='Add to cart', callback_data=f'add_{product.id}'),
        InlineKeyboardButton(text='View on site', url=f'{current_site()}{product.id}/{product.slug}/'),
        InlineKeyboardButton(text='Reviews', callback_data=f'reviews_{product.id}'),
        InlineKeyboardButton(text='Back ⬅️', callback_data=f'back_subcategory:{product.category.id}')
    ]
    reply_markup = InlineKeyboardMarkup(build_menu(button_list, n_cols=2))

    query.delete_message()
    query.message.reply_photo(photo=photo_url, caption=caption, reply_markup=reply_markup, parse_mode=ParseMode.HTML)


@debug_requests
def product_reviews_handler(update: Update, id: int, context: CallbackContext):
    query = update.callback_query
    product = Product.objects.get(pk=id)
    reviews = Review.objects.filter(product=product, status='True').order_by('-created')

    button_list = []
    for review in reviews:
        text = f'{review.user.username}, {review.created.strftime("%Y-%m-%d %H:%M")}, {review.rate}/5'
        button_list.append(InlineKeyboardButton(text=text, callback_data=f"review_{review.id}"))
    button_list.append(InlineKeyboardButton(text='Back ⬅️', callback_data=f'product_{id}'))
    reply_markup = InlineKeyboardMarkup(build_menu(button_list, n_cols=1))

    query.delete_message()
    if len(reviews) == 0:
        query.message.reply_text(text='<b>This product has no reviews</b>', reply_markup=reply_markup, parse_mode=ParseMode.HTML)
    else:
        query.message.reply_text(text=f'Reviews for <b>{product.name}</b>:', reply_markup=reply_markup, parse_mode=ParseMode.HTML)


def review_handler(update: Update, id: int, context: CallbackContext):
    query = update.callback_query
    review = Review.objects.get(pk=id)

    rate = review.rate
    text = f'<b>{review.user.username}</b>|<i>{review.created.strftime("%Y-%m-%d %H:%M")}</i>\n{"⭐️" * rate}{"❌" * (5-rate)}\n'
    text += f'{review.body}\n\n<b>Advantages: </b>{review.advantages}\n<b>Disadvantages: </b>{review.disadvantages}\n'
    text += f'👍({review.votes.likes().count()}) 👎({review.votes.dislikes().count()})\n'

    button_list = [
        InlineKeyboardButton(text='Back ⬅️', callback_data=f'reviews_{review.product.id}')
    ]
    reply_markup = InlineKeyboardMarkup(build_menu(button_list, n_cols=2))
    query.edit_message_text(text=text, reply_markup=reply_markup, parse_mode=ParseMode.HTML)
