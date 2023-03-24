import time

import stripe
from django.conf import settings
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from telegram.ext import CallbackContext, ConversationHandler

from cart.models import UserCart
from coupons.models import Coupon
from orders.models import Order, OrderItem, Delivery
from orders.utils import unique_order_id
from store.models import Product
from telegram_bot.handlers.cart_handler import get_cart
from telegram_bot.utils import build_menu, debug_requests, get_line_items, unique_code

PAYMENT, PAYMENT_CHECK = range(14, 16)
stripe.api_key = settings.STRIPE_TOKEN


@debug_requests
def confirm_info_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    data = query.data.split('_')[1]
    if data == 'yes':
        buttons = [
            InlineKeyboardButton(text='Cash', callback_data='payment_cash'),
            InlineKeyboardButton(text='Card', callback_data='payment_card')
        ]
        reply_markup = InlineKeyboardMarkup(build_menu(buttons, n_cols=2))
        query.edit_message_text(text='❕*Choose payment method*', reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)

        return PAYMENT
    else:
        query.edit_message_text('⚠️You have canceled your order')
        context.user_data.clear()
        return ConversationHandler.END


def create_order(cart: UserCart, context: CallbackContext, payment: str):
    order = Order.objects.create(
        order_id=context.user_data['order_id'],
        customer_first_name=context.user_data['customer_first_name'],
        customer_last_name=context.user_data['customer_last_name'],
        customer_email=context.user_data['customer_email'],
        customer_phone=context.user_data['phone'],
        recipient_first_name=context.user_data['recipient_first_name'],
        recipient_last_name=context.user_data['recipient_last_name'],
        recipient_email=context.user_data['recipient_email'],
        city=context.user_data['city'],
        address=context.user_data['address'],
        delivery=Delivery.objects.get(pk=context.user_data['delivery']),
        paymentMethod=payment,
        telegram_id=cart.chat_id
    )

    if 'coupon' in context.user_data:
        try:
            coupon = Coupon.objects.get(pk=context.user_data['coupon'])
            order.coupon = coupon
            order.discount = coupon.discount
        except: pass

    items_cart = dict(cart.items_cart)
    for product, item in items_cart.items():
        OrderItem.objects.create(
            order=order,
            product=Product.objects.get(pk=product),
            price=int(item['price']),
            quantity=int(item['quantity'])
        )

    cart.items_cart = []
    cart.save()

    return order


@debug_requests
def payment_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    data = query.data.split('_')[1]
    cart = get_cart(query.message.chat_id)
    context.user_data['order_id'] = unique_order_id()

    if data == 'cash':
        query.edit_message_text('✅ Your information was successfully saved')
        try:
            create_order(cart, context, data)
        except:
            query.edit_message_text(text="⚠️Something went wrong. Try again later")

        context.user_data.clear()
        return ConversationHandler.END
    else:
        #current_site = get_current_site(context.user_data['request'])
        current_time = int(time.time())
        line_items = get_line_items(cart, context.user_data['delivery_price'])

        if context.user_data['discount'] != 0:
            discount_price = context.user_data['total_price']*context.user_data['discount']
            coupon = stripe.Coupon.create(
                amount_off=discount_price,
                currency='uah',
                duration='once',
                name=f"{context.user_data['discount']}% off",
            )

            session = stripe.checkout.Session.create(
                payment_method_types=["card"],
                line_items=line_items,
                mode="payment",
                success_url=f"http://127.0.0.1:8000/",
                cancel_url=f"http://127.0.0.1:8000/",
                expires_at=current_time + 1800,
                discounts=[{"coupon": coupon.id}],
                billing_address_collection='auto'
            )
        else:
            session = stripe.checkout.Session.create(
                payment_method_types=["card"],
                line_items=line_items,
                mode="payment",
                success_url=f"http://127.0.0.1:8000/",
                cancel_url=f"http://127.0.0.1:8000/",
                expires_at=current_time + 1800
            )

        context.user_data["checkout_session_id"] = session.id

        checkout_url = session.url
        payment_message = "*Please click the button below to pay for your order:*\n" \
                          "_When you pay for the order, click the confirm button._"
        payment_keyboard = [
            InlineKeyboardButton(text="🛍️ Go to checkout", url=checkout_url),
            InlineKeyboardButton(text="Confirm", callback_data='confirm_order'),
        ]
        reply_markup = InlineKeyboardMarkup(build_menu(payment_keyboard, 1), resize_keyboard=True, one_time_keyboard=True)
        query.edit_message_text(payment_message, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)

        return PAYMENT_CHECK


@debug_requests
def payment_check_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    cart = get_cart(query.message.chat_id)
    checkout_session_id = context.user_data["checkout_session_id"]

    session = stripe.checkout.Session.retrieve(checkout_session_id)
    payment_status = session.payment_status

    if payment_status == "paid":
        try:
            order = create_order(cart, context, 'card')
            order.paid = True
            order.save()

            query.edit_message_text(text="✅ Payment successful! Thank you for your purchase.")
        except:
            query.edit_message_text(text="⚠️Something went wrong. Try again later")
    else:
        query.edit_message_text(text="⚠️Payment failed. Please try again.")
        stripe.checkout.Session.expire(context.user_data["checkout_session_id"])

    context.user_data.clear()
    return ConversationHandler.END