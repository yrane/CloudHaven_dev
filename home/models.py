from django.db import models
from django.contrib.auth.models import User
from jsonfield import JSONField

# from django.dispatch import receiver
# from django.db.models.signals import post_save

# class MyUser(User):
#     user = models.OneToOneField(User)
#     provider = models.CharField(max_length=32)
#     uid = models.CharField(max_length=255)
#     access_token = models.CharField(max_length=255)

class UserConnection(models.Model):
    user = models.ForeignKey(User, related_name='connections')
    provider = models.CharField(max_length=32)
    credentials = JSONField()

# @receiver(post_save, sender=User)
# def handle_user_save(sender, instance, created, **kwargs):
#     if created:
#         # print instance.username
#         # MyUser.objects.create(user=instance)
#
