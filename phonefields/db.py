from django.db import models

from .validator import clean_phone, PhoneValidatorMixin, PhoneFieldValidator
from . import forms


class FullPhoneField(PhoneValidatorMixin, models.CharField):
    _max_length = 20
    default_validators = [PhoneFieldValidator()]

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('max_length', self._max_length)
        super().__init__(*args, **kwargs)

    def pre_save(self, model_instance, add):
        value = getattr(model_instance, self.attname)
        value = clean_phone(value, **self.validator_options)
        setattr(model_instance, self.attname, value)

        return super().pre_save(model_instance, add)

    def formfield(self, **kwargs):
        kwargs['form_class'] = forms.FullPhoneField
        return super().formfield(**kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()

        if kwargs['max_length'] == self._max_length:
            kwargs.pop('max_length')

        kwargs.update(self.validator_options)

        return name, path, args, kwargs
