from django import forms

from .validator import PhoneValidatorMixin, clean_phone


class FullPhoneField(PhoneValidatorMixin, forms.CharField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('max_length', 20)
        super().__init__(*args, **kwargs)

    def clean(self, value):
        return clean_phone(value, **self.validator_options)
