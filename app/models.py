from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .multichain import api
from hashlib import md5
from json import dumps


class Account(models.Model):
    user = models.ForeignKey(User, related_name='account')
    account_name = models.CharField(max_length=255)
    account_number = models.CharField(max_length=255)


class UserStream(models.Model):
    user = models.OneToOneField(User)
    stream_id = models.CharField(max_length=32)


@receiver(post_save, sender=User)
def create_user_stream(sender, instance, created, **kwargs):
    if created:
        address = api.getnewaddress()
        stream_id = md5(address.encode('utf-8')).hexdigest()
        transaction_id = api.create('stream', stream_id, False)
        if not len(transaction_id) == 64:
            print('invalid transaction id (' + transaction_id + ')')

        user_stream = UserStream(user_id=instance.id, stream_id=stream_id)
        user_stream.save()


@receiver(post_save, sender=Account)
def publish_account_stream(sender, instance, created, **kwargs):
    if created:
        stream_id = instance.user.userstream.stream_id
        data = instance.account_name + '|' + instance.account_number
        api.publish(stream_id, 'account', data.encode('utf-8').hex())
