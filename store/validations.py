import re

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import datetime


def validate_discount(value):
    if value > 100:
        raise ValidationError(
            _('%(value)s is not correct discount'),
            params={'value': value},
        )


def validate_price(value):
    if value <= 0:
        raise ValidationError(
            _('%(value)s is not correct price'),
            params={'value': value},
        )


def validate_product_year(value):
    if value < 2005 or value > datetime.datetime.now().year:
        raise ValidationError(
            _('%(value)s is not correct year'),
            params={'value': value},
        )


class NumberValidator(object):
    def validate(self, password, user=None):
        if not re.findall('\d', password):
            raise ValidationError(
                _("The password must contain at least 1 digit, 0-9."),
                code='password_no_number',
            )

    def get_help_text(self):
        return _(
            "Your password must contain at least 1 digit, 0-9."
        )


class LowercaseValidator(object):
    def validate(self, password, user=None):
        if not re.findall('[a-z]', password):
            raise ValidationError(
                _("The password must contain at least 1 lowercase letter, a-z."),
                code='password_no_lower',
            )

    def get_help_text(self):
        return _(
            "Your password must contain at least 1 lowercase letter, a-z."
        )

