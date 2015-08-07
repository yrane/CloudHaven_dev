# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_auto_20150402_2233'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userconnection',
            name='user',
            field=models.ForeignKey(related_name=b'connections', to=settings.AUTH_USER_MODEL),
        ),
    ]
