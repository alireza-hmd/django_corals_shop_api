from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
import re


def letter_validator(password):
    regex = re.compile('[a-zA-Z]')
    if regex.search(password) == None:
        raise ValidationError(
            _('password must include letters'),
            code='password_must_include_letters'
        )


def number_validator(password):
    regex = re.compile('[0-9]')
    if regex.search(password) == None:
        raise ValidationError(
            _('password must include numbers'),
            code='password_must_include_numbers'
        )


def special_char_validator(password):
    regex = re.compile('[@_!#$%^&*()<>?/|\}{~:]')
    if regex.search(password) == None:
        raise ValidationError(
            _('password must include special characters'),
            code='password_must_include_special_chars'
        )
