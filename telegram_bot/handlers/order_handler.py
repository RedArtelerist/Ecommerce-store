from telegram import *
from telegram.ext import CallbackContext

from orders.models import Order
from telegram_bot.utils import build_menu, debug_requests, logger


def get_orders_buttons(chat_id):
    orders = Order.objects.filter(telegram_id=chat_id, available=True).order_by('-created')

    if len(orders) == 0:
        raise Exception('⚠️<b>You have no orders</b>')

    buttons = []
    for order in orders:
        buttons.append(InlineKeyboardButton(
            text=f'#{order.order_id} ({order.created.strftime("%d.%m.%Y %H:%M")})',
            callback_data=f'order_{order.id}')
        )
    reply_markup = InlineKeyboardMarkup(build_menu(buttons, n_cols=1))
    return reply_markup


@debug_requests
def user_orders_list_handler(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    try:
        update.message.delete()
        context.bot.delete_message(chat_id=chat_id, message_id=context.user_data['last_order_msg'])
    except: pass

    try:
        reply_markup = get_orders_buttons(chat_id)
        update.message.reply_text(text='Your orders:', reply_markup=reply_markup)
        context.user_data['last_order_msg'] = update.message.message_id + 1
    except Exception as ex:
        update.message.reply_text(text=str(ex), parse_mode=ParseMode.HTML)


@debug_requests
def back_to_user_orders_list_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    chat_id = query.message.chat_id

    try:
        reply_markup = get_orders_buttons(chat_id)
        query.edit_message_text(text='Your orders:', reply_markup=reply_markup)
    except Exception as ex:
        query.edit_message_text(text=str(ex), parse_mode=ParseMode.HTML)


def get_order_info(order: Order):
    dlm = '---------------------------------------------------------------------'
    general = f'Order <code>#{order.order_id}</code>\n<b>{order.created.strftime("%d.%m.%Y %H:%M")}</b>\n<b>Status</b>: <i>{order.status}</i>\n'

    if order.paymentMethod == 'cash':
        general += '<b>Payment:</b> 💵\n'
    else:
        general += '<b>Payment:</b> 💳\n'

    if order.paid:
        general += '<b>Paid:</b> ✅\n'
    else:
        general += '<b>Paid:</b> ⛔️\n'

    items = []
    for item in order.items.all():
        items.append(f'<b>{item.product.name}</b>:\n<code>₴{item.price} x {item.quantity} — ₴{item.get_cost()}</code>\n')
    order_info = f'<pre>Your order:</pre>\n{dlm}\n' + '\n'.join(items)
    order_info += f'\n<b>Total</b>: <code>₴{order.get_total_cost()}</code>'
    order_info += f'\n<b>Delivery:</b> <code>₴{order.delivery.price}</code>\n'

    if order.discount != 0:
        order_info += f'<b>Discount:</b> <code>-₴{order.get_discount()}(-{order.discount}%)</code>\n'

    order_info += f'<b>Grand total:</b> <code>₴{order.get_grand_total_cost()}</code>\n'

    personal_info = f'<pre>Your personal info:</pre>\n' \
                    f'<b>First name:</b> <i>{order.customer_first_name}</i>\n' \
                    f'<b>Last name:</b> <i>{order.customer_last_name}</i>\n' \
                    f'<b>Email:</b> <i>{order.customer_email}</i>\n' \
                    f'<b>Phone:</b> <i>{order.customer_phone}</i>\n'

    recipient_info = f'<pre><b>Recipient info:</b></pre>\n' \
                     f'<b>First name:</b> <i>{order.recipient_first_name}</i>\n' \
                     f'<b>Last name:</b> <i>{order.recipient_last_name}</i>\n' \
                     f'<b>Email:</b> <i>{order.recipient_email}</i>\n'

    address_info = f'<pre>Address:</pre>\n<i>{order.city}, {order.address}</i>'

    info = f'{general}{dlm}\n{order_info}{dlm}\n{personal_info}{dlm}\n{recipient_info}{dlm}\n{address_info}'
    return info


@debug_requests
def order_detail_handler(update: Update, context: CallbackContext, id: int):
    query = update.callback_query
    chat_id = query.message.chat_id

    order = Order.objects.filter(pk=id).first()
    if order is None:
        query.answer('Something went wrong')
        try:
            query.delete_message()
            query.message.reply_text(text='Your orders:', reply_markup=get_orders_buttons(chat_id))
        except Exception as ex:
            query.edit_message_text(text=str(ex), parse_mode=ParseMode.HTML)
    else:
        buttons = []
        if order.status == 'New' or order.status == 'Accepted' or order.status == 'Preparing':
            buttons.append(InlineKeyboardButton(text='Cancel', callback_data=f'cancel_{order.id}'))
        buttons.append(InlineKeyboardButton(text='Delete', callback_data=f'delete-order_{order.id}'))
        buttons.append(InlineKeyboardButton(text='Back', callback_data='back_orders'))
        reply_markup = InlineKeyboardMarkup(build_menu(buttons, n_cols=2))
        query.edit_message_text(text=get_order_info(order), reply_markup=reply_markup, parse_mode=ParseMode.HTML)


@debug_requests
def order_cancel_handler(update: Update, context: CallbackContext, id: int):
    query = update.callback_query
    chat_id = query.message.chat_id

    order = Order.objects.filter(pk=id).first()
    if order is None:
        query.answer('Something went wrong')
        try:
            query.delete_message()
            query.message.reply_text(text='Your orders:', reply_markup=get_orders_buttons(chat_id))
        except Exception as ex:
            query.edit_message_text(text=str(ex))
    else:
        if order.status != 'New' and order.status != 'Accepted' and order.status != 'Preparing':
            query.answer('You can\'t cancel this order')
        else:
            order.status = 'Canceled'
            order.save()
            query.answer('This order was successfully canceled')
        query.edit_message_text(text='Your orders:', reply_markup=get_orders_buttons(chat_id))


@debug_requests
def order_delete_handler(update: Update, context: CallbackContext, id: int):
    query = update.callback_query
    chat_id = query.message.chat_id

    order = Order.objects.filter(pk=id).first()
    if order is None:
        query.answer('Something went wrong')
        try:
            query.delete_message()
            query.message.reply_text(text='Your orders:', reply_markup=get_orders_buttons(chat_id))
        except Exception as ex:
            query.edit_message_text(text=str(ex))
    else:
        order.available = False
        order.save()
        query.answer('This order was successfully deleted')
        query.edit_message_text(text='Your orders:', reply_markup=get_orders_buttons(chat_id))