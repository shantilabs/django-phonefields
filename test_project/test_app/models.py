from django.db import models
from phonefields import FullPhoneDbField

class SampleModel(models.Model):
    phone = FullPhoneDbField()


class SampleModelUSA(models.Model):
    phone = FullPhoneDbField(default_code='1')
