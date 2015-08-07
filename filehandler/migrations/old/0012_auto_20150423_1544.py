# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('filehandler', '0011_auto_20150423_1539'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userfile_chunks',
            name='file_id',
        ),
        migrations.DeleteModel(
            name='UserFile_Chunks',
        ),
    ]
