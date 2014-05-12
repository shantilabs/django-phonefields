django-phonefields
==================

Install:

    pip install -e git+https://github.com/shantilabs/django-phonefields#egg=phonefields

Add to installed apps (for localization support):

    INSTALLED_APPS = (
        # ....
        'phonefields',
    )

Usage:

    from phonefields import FullPhoneDbField, FullPhoneFormField

Optional settings:

    # allow russian and ukrainian numbers only
    AVAILABLE_PHONE_COUNTRY_CODES = ('7', '380')

    # allow all codes by default
    AVAILABLE_PHONE_COUNTRY_CODES = None

    # default value for numbers without country code
    DEFAULT_PHONE_COUNTRY_CODE = '7'
