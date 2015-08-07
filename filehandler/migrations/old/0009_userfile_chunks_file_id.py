# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('filehandler', '0008_remove_userfile_chunks_f_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='userfile_chunks',
            name='file_id',
            field=models.ForeignKey(default=1, to='filehandler.UserFile'),
            preserve_default=False,
        ),
    ]
