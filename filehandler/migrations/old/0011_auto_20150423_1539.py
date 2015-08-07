# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('filehandler', '0010_auto_20150423_1537'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userfile_chunks',
            name='file_id',
            field=models.ForeignKey(to='filehandler.UserFile'),
            preserve_default=True,
        ),
    ]
