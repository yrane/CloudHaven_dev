# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('filehandler', '0007_auto_20150423_1535'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userfile_chunks',
            name='f_id',
        ),
    ]
