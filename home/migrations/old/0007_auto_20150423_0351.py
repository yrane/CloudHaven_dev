# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_auto_20150423_0029'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userconnection',
            name='access_token',
        ),
        migrations.RemoveField(
            model_name='userconnection',
            name='refresh_token',
        ),
        migrations.RemoveField(
            model_name='userconnection',
            name='uid',
        ),
        migrations.AddField(
            model_name='userconnection',
            name='credentials',
            field=jsonfield.fields.JSONField(default=None),
            preserve_default=False,
        ),
    ]
