# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('filehandler', '0009_userfile_chunks_file_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userfile_chunks',
            name='file_id',
            field=models.CharField(max_length=255),
            preserve_default=True,
        ),
    ]
