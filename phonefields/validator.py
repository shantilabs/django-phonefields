import re

from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.encoding import force_text
from django.utils.translation import ugettext

from .codes import all_codes


class PhoneFieldValidator:
    OPTIONS = (
        'available_codes',
        'default_code',
        'min_phone_length',
        'max_phone_length',
        'max_full_phone_length',
        'required',
    )

    def __init__(self, **options):
        self.options = options

    def __call__(self, value):
        return clean_phone(value, **self.options)


def clean_phone(
    value,
    available_codes=None,
    default_code=None,
    min_length=8,
    max_length=10,
    max_full_phone_length=15,
    required=True,
):
    if default_code is None:
        default_code = getattr(settings, 'DEFAULT_PHONE_COUNTRY_CODE', '7')

    if available_codes is None:
        available_codes = getattr(settings, 'AVAILABLE_PHONE_COUNTRY_CODES', None) or all_codes

    if not value and not required:
        return value

    value = force_text(value)
    value = value.strip()

    if not value and not required:
        return value

    phone = None
    code = None

    has_country_code = value.startswith('+')
    value = value.lstrip('+')
    value = re.sub(r'[^\d]', '', value)

    if not value or len(value) > max_full_phone_length:
        raise ValidationError(ugettext('Incorrect phone'))

    if value.startswith(default_code):
        phone = value[len(default_code):]
        code = default_code
    elif not has_country_code and (value.startswith('8') or value.startswith('9')):
        phone = value[1:] if value.startswith('8') else value
        code = default_code
    else:
        for c in available_codes:
            if value.startswith(c):
                phone = value[len(c):]
                code = c
                break
        if not phone:
            raise ValidationError(ugettext('Unsupported country code'))

    length = len(phone)
    if not (min_length <= length <= max_length):
        raise ValidationError(ugettext('Incorrect phone length'))

    return '+' + code + phone
