import stripe
from django.utils import timezone
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, ParseMode
from telegram.ext import CallbackContext, ConversationHandler

from coupons.models import Coupon
from telegram_bot.buttons import regions_reply_markup
from telegram_bot.utils import *
from telegram_bot.handlers.validators import *

C_FIRST_NAME, C_LAST_NAME, PHONE, C_EMAIL, RECIPIENT, R_FIRST_NAME, R_LAST_NAME, R_EMAIL, COUPON,  REGION = range(10)


@debug_requests
def start_order_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    init = update.callback_query.data
    logger.info(init)

    if init != 'checkout_start':
        update.callback_query.bot.send_message(
            chat_id=query.message.chat_id,
            text='Something went wrong',
        )
        return ConversationHandler.END
    query.edit_message_text(
        text='Please provide some information to place an order. If you want to cancel your order write /cancel.\n\n❕*Now enter your name:*',
        parse_mode=ParseMode.MARKDOWN
    )
    return C_FIRST_NAME


@debug_requests
def customer_first_name_handler(update: Update, context: CallbackContext):
    try:
        logger.info('C_FIRST_NAME: ' + update.message.text)
        first_name = validate_name(update.message.text, 'name')
        context.user_data['customer_first_name'] = first_name
        update.message.reply_text(text='❕*Enter your surname:*', parse_mode=ParseMode.MARKDOWN)
        return C_LAST_NAME
    except Exception as ex:
        update.message.reply_text(f'❗️ {str(ex)}')
        return C_FIRST_NAME


@debug_requests
def customer_last_name_handler(update: Update, context: CallbackContext):
    try:
        logger.info('C_LAST_NAME: ' + update.message.text)
        last_name = validate_name(update.message.text, 'surname')
        context.user_data['customer_last_name'] = last_name
        update.message.reply_text(text='❕*Enter your email:*', parse_mode=ParseMode.MARKDOWN)
        return C_EMAIL
    except Exception as ex:
        update.message.reply_text(f'❗️ {str(ex)}')
        return C_LAST_NAME


@debug_requests
def customer_email_handler(update: Update, context: CallbackContext):
    try:
        logger.info('C_EMAIL: ' + update.message.text)
        email = validate_email(update.message.text)
        context.user_data['customer_email'] = email

        update.message.reply_text(
            text='❕*Enter your phone* (like _+380xxxxxxxxx_):',
            parse_mode=ParseMode.MARKDOWN
        )
        return PHONE
    except Exception as ex:
        update.message.reply_text(f'❗️ {str(ex)}')
        return C_EMAIL


@debug_requests
def customer_phone_handler(update: Update, context: CallbackContext):
    try:
        logger.info('PHONE: ' + update.message.text)
        phone = validate_phone(update.message.text)
        context.user_data['phone'] = phone

        button_list = [
            InlineKeyboardButton(text='Yes', callback_data='recip_yes'),
            InlineKeyboardButton(text='No', callback_data='recip_no'),
        ]
        reply_markup = InlineKeyboardMarkup(build_menu(button_list, n_cols=2))

        info = f'`Your personal info:`\n' \
               f'*First name:* _{context.user_data["customer_first_name"]}_\n' \
               f'*Last name:* _{context.user_data["customer_last_name"]}_\n' \
               f'*Email:* _{context.user_data["customer_email"]}_\n' \
               f'*Phone:* _{context.user_data["phone"]}_\n\nAre you a recipient?'
        update.message.reply_text(text=info, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)

        return RECIPIENT
    except Exception as ex:
        update.message.reply_text(f'❗️ {str(ex)}')
        return PHONE


@debug_requests
def recipient_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    data = query.data.split('_')[1]
    logger.info('RECIPIENT: ' + data)
    if data == 'yes':
        context.user_data['recipient_first_name'] = context.user_data['customer_first_name']
        context.user_data['recipient_last_name'] = context.user_data['customer_last_name']
        context.user_data['recipient_email'] = context.user_data['customer_email']

        query.edit_message_text(
            text='❕Now enter the promo code if you have one. Otherwise, enter *skip* to go to a next step',
            parse_mode=ParseMode.MARKDOWN
        )
        return COUPON

    context.user_data['recipient'] = False
    query.edit_message_text(text='❕*Enter recipient name*', parse_mode=ParseMode.MARKDOWN)
    return R_FIRST_NAME


@debug_requests
def recipient_first_name_handler(update: Update, context: CallbackContext):
    try:
        logger.info('R_FIRST_NAME: ' + update.message.text)
        first_name = validate_name(update.message.text, 'name')
        context.user_data['recipient_first_name'] = first_name

        update.message.reply_text(text='❕*Enter recipient surname:*', parse_mode=ParseMode.MARKDOWN)
        return R_LAST_NAME
    except Exception as ex:
        update.message.reply_text(f'❗️ {str(ex)}')
        return R_FIRST_NAME


@debug_requests
def recipient_last_name_handler(update: Update, context: CallbackContext):
    try:
        logger.info('R_LAST_NAME: ' + update.message.text)
        last_name = validate_name(update.message.text, 'surname')
        context.user_data['recipient_last_name'] = last_name

        update.message.reply_text(text='❕*Enter recipient email:*', parse_mode=ParseMode.MARKDOWN)
        return R_EMAIL
    except Exception as ex:
        update.message.reply_text(f'❗️ {str(ex)}')
        return R_LAST_NAME


@debug_requests
def recipient_email_handler(update: Update, context: CallbackContext):
    try:
        logger.info('R_EMAIL: ' + update.message.text)
        email = validate_email(update.message.text)
        context.user_data['recipient_email'] = email

        update.message.reply_text(
            text='❕Now enter the promo code if you have one. Otherwise, enter *skip* to go to a next step',
            parse_mode=ParseMode.MARKDOWN
        )
        return COUPON

    except Exception as ex:
        update.message.reply_text(f'❗️ {str(ex)}')
        return R_EMAIL


@debug_requests
def coupon_handler(update: Update, context: CallbackContext):
    text = update.message.text
    logger.info('COUPON: ' + update.message.text)
    now = timezone.now()
    if text != 'skip':
        try:
            coupon = Coupon.objects.get(
                code__iexact=text, valid_from__lte=now,
                valid_to__gte=now, active=True
            )
            context.user_data['coupon'] = coupon.id
            update.message.reply_text(f'✅  You entered the correct promo code that gives you a {coupon.discount}% discount on your entire order.')
        except:
            update.message.reply_text(f'❗️ Coupon not found. Try again or enter "skip" to go to a next step')
            return COUPON

    update.message.reply_text(
        text='❕Now you need to select a delivery address. To begin with, indicate the *region* in which you are located.',
        reply_markup=regions_reply_markup(),
        parse_mode=ParseMode.MARKDOWN
    )
    return REGION


@debug_requests
def cancel_handler(update: Update, context: CallbackContext):
    logger.info('Cancel: ' + update.message.text)
    update.message.reply_text('⚠️Your order was canceled')
    try:
        stripe.checkout.Session.expire(context.user_data["checkout_session_id"])
    except: pass
    context.user_data.clear()

    return ConversationHandler.END