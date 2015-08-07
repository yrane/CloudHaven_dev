# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserFile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('file', models.FileField(null=True, upload_to=b'')),
                ('name', models.CharField(max_length=255)),
                ('user', models.ForeignKey(related_name='files', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserFileChunks',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('service', models.CharField(max_length=255)),
                ('identifier', models.CharField(max_length=1000)),
                ('name', models.CharField(max_length=1000)),
                ('file_id', models.ForeignKey(related_name='chunks', to='filehandler.UserFile')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
