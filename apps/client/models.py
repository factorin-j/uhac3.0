from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from werkzeug.security import gen_salt


class Account(models.Model):
    user = models.OneToOneField(User, null=True, blank=True)
    account_name = models.CharField(max_length=255)
    account_number = models.CharField(max_length=255)


class UserStream(models.Model):
    user = models.OneToOneField(User)
    stream_id = models.CharField(max_length=32)


@receiver(post_save, sender=User)
def create_user_stream(sender, instance, created, **kwargs):
    if created:
        user_stream = UserStream(user_id=instance.id, stream_id=gen_salt(32))
        user_stream.save()
