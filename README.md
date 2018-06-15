django-phonefields
==================


[![Build Status](https://travis-ci.org/shantilabs/django-phonefields.svg?branch=master)](https://travis-ci.org/shantilabs/django-phonefields)


Simple django form and model fields that performs validation and normalizatio of phone numbers. Tested with Python 2.7, 3.6 and the latest django in 1.x and 2.x branches.


Install:
```
    pip install -e git+https://github.com/shantilabs/django-phonefields#egg=phonefields
```

Add to installed apps (for localization support):
```python
    INSTALLED_APPS = (
        # ....
        'phonefields',
    )
```

Usage in forms:
```python
    from phonefields import FullPhoneFormField

    class MyForm(forms.Form):
        phone = FullPhoneFormField()

    form = MyForm({'phone': ' (923-112 33 11  '})
    assert form.is_valid()
    print(form.cleaned_data['phone'])  # +79231123311
```


And in models:
```python
    from phonefields import FullPhoneDbField

    class MyModel(models.Model):
        phone = FullPhoneDbField(default_code='1')

    object = MyModel.objects.create(phone='  332-111 22 33.')

    print(object.phone)  # +13321112233
```

Optional settings:
```python
    # allow russian and ukrainian numbers only
    AVAILABLE_PHONE_COUNTRY_CODES = ('7', '380')

    # allow all codes by default
    AVAILABLE_PHONE_COUNTRY_CODES = None

    # default value for numbers without country code
    DEFAULT_PHONE_COUNTRY_CODE = '7'
```
