from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .multichain import api
from hashlib import md5


class CriminalRecord(models.Model):
    user = models.ForeignKey(User, related_name='records')
    offense = models.TextField()
    case_number = models.IntegerField(unique=True)
    case_status = models.CharField(max_length=255)
    committed_at = models.DateTimeField()


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


@receiver(post_save, sender=CriminalRecord)
def publish_criminal_record_stream(sender, instance, created, **kwargs):
    if created:
        stream_id = instance.user.userstream.stream_id
        data = str('|').join([
            instance.offense,
            instance.case_number,
            instance.case_status,
            str(instance.committed_at),
        ])
        api.publish(stream_id, 'records', data.encode('utf-8').hex())
