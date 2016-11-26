from django.db import models
from django.contrib.auth.models import User


class Account(models.Model):
    user = models.OneToOneField(User, null=True, blank=True)
    account_name = models.CharField(max_length=255)
    account_number = models.CharField(max_length=255)


class UserStream(models.Model):
    user = models.OneToOneField(User)
    stream_id = models.CharField(max_length=32)
