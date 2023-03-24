from email.mime.image import MIMEImage
from functools import lru_cache

from django.contrib.sites.shortcuts import get_current_site
from django.contrib.staticfiles import finders
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from EcommerceStore import settings


def orderMail(request, order):
    current_site = get_current_site(request)
    mail_subject = 'Order Confirmation.'

    html_content = render_to_string('orders/order_mail.html', {
        'order': order,
        'domain': current_site.domain,
        'protocol': 'http',
    })

    text_content = strip_tags(html_content)

    msg = EmailMultiAlternatives(mail_subject, text_content, settings.EMAIL_HOST_USER, [order.customer_email])
    msg.attach_alternative(html_content, "text/html")
    #logo_data(order, msg)
    msg.send(fail_silently=False)


@lru_cache()
def logo_data(order, msg):
    with open(finders.find('images/icons/logo.png'), 'rb') as f:
        logo_data = f.read()
    logo = MIMEImage(logo_data)
    logo.add_header('Content-ID', '<logo>')
    msg.attach(logo)

    n = 1
    for item in order.items.all():
        product = item.product
        fp = open(finders.find('images/' + str(product.image)), 'rb')
        msgImage = MIMEImage(fp.read())
        fp.close()
        msgImage.add_header('Content-ID', '<image' + str(n) + '>')
        msg.attach(msgImage)
        n += 1

