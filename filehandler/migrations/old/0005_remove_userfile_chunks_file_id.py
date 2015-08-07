# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('filehandler', '0004_userfile_chunks'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userfile_chunks',
            name='file_id',
        ),
    ]
