import pytest
from django.forms import forms

from phonefields import FullPhoneFormField, FullPhoneDbField

from test_app.models import SampleModelUSA, SampleModel


@pytest.mark.parametrize('value,expected', (
    (u'79254525700', u'+79254525700'),
    (b'9161234567', u'+79161234567'),
    ('89161234567', u'+79161234567'),
    ('+7(916)1234567', u'+79161234567'),
    ('(916)1234567', u'+79161234567'),
    (u' 8(916)-123-45-67 ', u'+79161234567'),
    (u'+37412345678', u'+37412345678'),
))
def test_validation(value, expected):
    """
    Test form field validation and cleaning
    """

    clean_value = FullPhoneFormField().clean(value)

    assert clean_value == expected


def test_form():
    """
    Test that validation runs in form context
    """
    class Form(forms.Form):
        phone = FullPhoneFormField()

    assert Form({'phone': '          '}).is_valid() is False

    assert Form({'phone': '8(923 999-22-33 '}).is_valid()
    assert Form({'phone': '+7 999 233-11-22'}).is_valid()

    class OptionalForm(forms.Form):
        phone = FullPhoneFormField(required=False)
    assert OptionalForm({'phone': ''}).is_valid()


@pytest.mark.django_db
def test_model_field():
    """
    Check that values are preprocessed when the model is saved
    """
    obj = SampleModel.objects.create(phone='8923 111 22 33')

    assert obj.phone == '+79231112233'


@pytest.mark.django_db
def test_model_field_with_options():
    """
    Check that field attributes are parsed correctly.

    In this case field have 'default' argument
    """
    obj = SampleModelUSA.objects.create(phone='8923 111 22 33')

    assert obj.phone == '+19231112233'


@pytest.mark.django_db
def test_deconstruct():
    """
    Test field deconstruction
    """
    original = FullPhoneDbField(default='1', max_phone_length=8, min_phone_length=1)
    name, path, args, kwargs = original.deconstruct()

    copy = FullPhoneDbField(*args, **kwargs)

    assert original.validator_options == copy.validator_options
    assert original.max_length == copy.max_length


@pytest.mark.django_db
def test_deconstruct_default():
    """
    Test field deconstruction (when no arguments passed)
    """
    original = FullPhoneDbField()
    name, path, args, kwargs = original.deconstruct()

    copy = FullPhoneDbField(*args, **kwargs)

    assert original.validator_options == copy.validator_options
    assert original.max_length == copy.max_length
