django-phonefields
==================

Usage:

    from phonefields import FullPhoneDbField, FullPhoneFormField

Optional settings:

    # allow russian and ukrainian numbers only
    AVAILABLE_PHONE_COUNTRY_CODES = ('7', '380')

    # allow all (by default)
    AVAILABLE_PHONE_COUNTRY_CODES = None

    # add
    DEFAULT_PHONE_COUNTRY_CODE = '7'
