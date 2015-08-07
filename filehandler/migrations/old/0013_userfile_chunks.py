# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('filehandler', '0012_auto_20150423_1544'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserFile_Chunks',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('service', models.CharField(max_length=255)),
                ('file', models.FileField(null=True, upload_to=b'')),
                ('name', models.CharField(max_length=255)),
                ('file_id', models.ForeignKey(to='filehandler.UserFile')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
