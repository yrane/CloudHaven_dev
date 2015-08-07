# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_userconnection_refresh_token'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userconnection',
            name='refresh_token',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
