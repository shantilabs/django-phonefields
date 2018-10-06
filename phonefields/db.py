from django.db import models

from . import forms
from .validator import PhoneFieldValidator


class FullPhoneField(models.CharField):
    _max_length = 20
    default_validators = [PhoneFieldValidator()]

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('max_length', self._max_length)
        self.validator_options = {}
        for k in PhoneFieldValidator.OPTIONS:
            if k in kwargs:
                self.validator_options[k] = kwargs.pop(k)
        super().__init__(*args, **kwargs)
        for i, v in enumerate(self.validators):
            if not isinstance(v, PhoneFieldValidator):
                continue
            if self.blank or self.null:
                self.validator_options['required'] = False
            self.validators[i] = PhoneFieldValidator(**self.validator_options)

    def pre_save(self, model_instance, add):
        value = getattr(model_instance, self.attname)
        for v in self.validators:
            if isinstance(v, PhoneFieldValidator):
                value = v(value)
        setattr(model_instance, self.attname, value)
        return super().pre_save(model_instance, add)

    def formfield(self, **kwargs):
        kwargs.update(**self.validator_options)
        kwargs['form_class'] = forms.FullPhoneField
        return super().formfield(**kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()

        if kwargs['max_length'] == self._max_length:
            kwargs.pop('max_length')

        kwargs.update(self.validator_options)

        return name, path, args, kwargs
