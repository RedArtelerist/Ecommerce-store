from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from EcommerceStore import settings
from telegram_bot.utils import current_site


def orderMail(request, order):
    curr_site = get_current_site(request)
    if request is None:
        domain = current_site().split('://')[1]
    else:
        domain = curr_site.domain
    mail_subject = 'Order Confirmation.'

    html_content = render_to_string('orders/order_mail.html', {
        'order': order,
        'domain': domain,
        'protocol': 'https',
    })

    text_content = strip_tags(html_content)

    msg = EmailMultiAlternatives(mail_subject, text_content, settings.EMAIL_HOST_USER, [order.customer_email])
    msg.attach_alternative(html_content, "text/html")
    msg.send(fail_silently=False)

