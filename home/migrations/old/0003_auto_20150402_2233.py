# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_auto_20150402_1127'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userconnection',
            old_name='connections',
            new_name='user',
        ),
    ]
