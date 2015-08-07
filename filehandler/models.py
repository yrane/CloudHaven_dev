# -*- coding: utf-8 -*-
from django import forms

class UserFileForm(forms.Form):
    file = forms.FileField()

# -------------------------------------------------

from django.db import models
from django.contrib.auth.models import User

class UserFile(models.Model):
    user = models.ForeignKey(User, related_name='files')
    file = models.FileField(null=True)
    name = models.CharField(max_length=255)


class UserFileChunks(models.Model):
    file_id = models.ForeignKey(UserFile, related_name='chunks')
    # file_id = models.CharField(max_length=255)
    # user = models.ForeignKey(User, related_name='files')
    service = models.CharField(max_length=255)
    identifier = models.CharField(max_length=1000)
    name = models.CharField(max_length=1000)

