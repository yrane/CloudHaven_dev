# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('filehandler', '0006_userfile_chunks_file_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userfile_chunks',
            old_name='file_id',
            new_name='f_id',
        ),
    ]
