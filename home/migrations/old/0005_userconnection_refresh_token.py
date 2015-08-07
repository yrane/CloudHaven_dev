# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_auto_20150405_0116'),
    ]

    operations = [
        migrations.AddField(
            model_name='userconnection',
            name='refresh_token',
            field=models.CharField(default=0, max_length=255),
            preserve_default=False,
        ),
    ]
