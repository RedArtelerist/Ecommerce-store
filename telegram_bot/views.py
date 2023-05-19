import json

from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt

from telegram_bot.buttons import *
from telegram_bot.handlers.cart_handler import *
from telegram_bot.handlers.checkout_handler import *
from telegram_bot.handlers.delivery_handler import *
from telegram_bot.handlers.order_handler import *
from telegram_bot.handlers.payment_handler import *
from telegram_bot.handlers.product_handler import *
from telegram_bot.utils import *


@debug_requests
def start_handler(update: Update, context: CallbackContext):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Hello! I'm a bot. What can I do for you?",
        reply_markup=get_base_reply_keyboard()
    )


@debug_requests
def button_callback_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    data = query.data
    logger.info(data)

    action = data
    val = ''

    try:
        action, val = data.split('_')
    except: pass

    if action == 'category':
        subcategories_handler(update, int(val), context)
    if action == 'subcategory':
        products_handler(update, int(val), context)
    if action == 'product':
        product_detail_handler(update, int(val), context)
    if action == 'reviews':
        product_reviews_handler(update, int(val), context)
    if action == 'review':
        review_handler(update, int(val), context)
    if action == 'add':
        add_to_cart(update, int(val), context)
        close_cart_handler(update, context)
    if action == 'plus':
        add_to_cart(update, int(val), context)
        edit_cart_handler(update, context)
    if action == 'minus':
        remove_from_cart(update, int(val), context)
        edit_cart_handler(update, context)
    if action == 'remove':
        remove_from_cart(update, int(val), context, True)
        edit_cart_handler(update, context)
    if action == 'clear' and val == 'cart':
        clear_cart_handler(update, context)
    if action == 'close' and val == 'cart':
        close_cart_handler(update, context)
    if action == 'edit' and val == 'cart':
        edit_cart_handler(update, context)
    if action == 'order':
        order_detail_handler(update, context, int(val))
    if action == 'delete-order':
        order_delete_handler(update, context, int(val))
    if action == 'cancel':
        order_cancel_handler(update, context, int(val))
    if action == 'back':
        if val == 'menu':
            query.edit_message_text('All categories:', reply_markup=get_categories_buttons())
        if val.startswith('subcategory'):
            id = int(val.split(':')[1])
            products_handler(update, id, context, False)
        if val == 'cart':
            get_cart_handler(update, context, True)
        if val == 'orders':
            back_to_user_orders_list_handler(update, context)


@debug_requests
def report_handler(update: Update, context: CallbackContext):
    update.message.reply_text(
        text="This is bot for online shopping\n\n"
             "The list of available commands is in the menu\n\n"
             "I also reply to any message.",
    )


@debug_requests
def echo_handler(update: Update, context: CallbackContext):
    text = update.message.text

    if text == BUTTON1_CATEGORIES:
        categories_handler(update, context)
    elif text == BUTTON2_CART:
        get_cart_handler(update, context)
    elif text == BUTTON3_REPORT:
        return report_handler(update, context)
    elif text == BUTTON4_ORDERS:
        return user_orders_list_handler(update, context)
    else:
        reply_text = 'Press any button below'
        update.message.reply_text(
            text=reply_text,
            reply_markup=get_base_reply_keyboard(),
        )


WEBHOOK_URL = f'{settings.TELEGRAM_WEBHOOK_URL}/telegram/'
BOT_TOKEN = settings.TELEGRAM_BOT_TOKEN
bot = Bot(token=BOT_TOKEN)
updater = Updater(token=BOT_TOKEN, use_context=True)
dispatcher = updater.dispatcher

conv_handler = ConversationHandler(
    entry_points=[
        CallbackQueryHandler(start_order_handler, pattern='checkout_start'),
    ],
    states={
        C_FIRST_NAME: [MessageHandler(Filters.text & ~Filters.command, customer_first_name_handler)],
        C_LAST_NAME: [MessageHandler(Filters.text & ~Filters.command, customer_last_name_handler)],
        C_EMAIL: [MessageHandler(Filters.text & ~Filters.command, customer_email_handler)],
        PHONE: [MessageHandler(Filters.text & ~Filters.command, customer_phone_handler)],
        RECIPIENT: [CallbackQueryHandler(recipient_handler)],
        R_FIRST_NAME: [MessageHandler(Filters.text & ~Filters.command, recipient_first_name_handler)],
        R_LAST_NAME: [MessageHandler(Filters.text & ~Filters.command, recipient_last_name_handler)],
        R_EMAIL: [MessageHandler(Filters.text & ~Filters.command, recipient_email_handler)],
        COUPON: [MessageHandler(Filters.text & ~Filters.command, coupon_handler)],
        REGION: [CallbackQueryHandler(region_handler)],
        CITY: [CallbackQueryHandler(city_handler)],
        ADDRESS: [MessageHandler(Filters.text & ~Filters.command, address_handler)],
        DELIVERY: [CallbackQueryHandler(delivery_handler)],
        CONFIRM: [CallbackQueryHandler(confirm_info_handler)],
        PAYMENT: [CallbackQueryHandler(payment_handler)],
        PAYMENT_CHECK: [CallbackQueryHandler(payment_check_handler)]
    },
    fallbacks=[
        CommandHandler('cancel', cancel_handler),
    ],
    conversation_timeout=0,
)

dispatcher.add_handler(conv_handler)
dispatcher.add_handler(CommandHandler('start', start_handler))
dispatcher.add_handler(CommandHandler('categories', categories_handler))
dispatcher.add_handler(CommandHandler('cart', get_cart_handler))
dispatcher.add_handler(CommandHandler('orders', user_orders_list_handler))
dispatcher.add_handler(CommandHandler('report', report_handler))
dispatcher.add_handler(CallbackQueryHandler(button_callback_handler))
dispatcher.add_handler(MessageHandler(Filters.all, echo_handler))

bot.setWebhook(WEBHOOK_URL)

@csrf_exempt
@debug_requests
def telegram_webhook(request):
    if request.method == 'POST':
        json_string = request.body.decode('utf-8')
        update = Update.de_json(json.loads(json_string), updater.bot)
        dispatcher.process_update(update)
        return HttpResponse(status=200)
    else:
        return HttpResponseBadRequest('Invalid request method')