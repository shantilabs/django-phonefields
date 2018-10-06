from django import forms

from .validator import clean_phone, PhoneFieldValidator


class FullPhoneField(forms.CharField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('max_length', 20)
        super().__init__(*args, **kwargs)
        self.validator_options = {k: v for k, v in kwargs.items()
                                  if k in PhoneFieldValidator.OPTIONS}

    def clean(self, value):
        return clean_phone(value, **self.validator_options)
