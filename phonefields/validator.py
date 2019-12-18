import re

from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.encoding import force_text
from django.utils.translation import ugettext

from .codes import all_codes

#  E.164 permits a maximum length of 15 digits for the complete
#  international phone number consisting of the country code,
#  the national routing code (area code), and the subscriber number
max_phone_length = 15
min_bare_phone_length = 8


class PhoneFieldValidator:
    OPTIONS = (
        'available_codes',
        'default_code',
        'required',
    )

    def __init__(self, **options):
        self.options = options

    def __call__(self, value):
        return clean_phone(value, **self.options)


def clean_phone(value, available_codes=None, default_code=None, required=True):
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

    code = None
    bare_phone = None

    value = re.sub(r'[^\d]', '', value.lstrip('+'))

    if value.startswith(default_code):
        bare_phone = value[len(default_code):]
        code = default_code
    elif value.startswith('9') and len(value) == 10:  # XXX:
        bare_phone = value
        code = default_code
    elif value.startswith('8'):
        bare_phone = value[1:]
        code = default_code
    else:
        for c in available_codes:
            if value.startswith(c):
                bare_phone = value[len(c):]
                code = c
                break
        if not bare_phone:
            raise ValidationError(ugettext('Unsupported country code'))

    result = '+' + code + bare_phone
    if len(bare_phone) < min_bare_phone_length or len(result) > max_phone_length:
        raise ValidationError(ugettext('Incorrect phone length'))

    return result
