# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('neptune', '0005_auto_20170110_1358'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='place',
            name='Address_Name',
        ),
        migrations.AddField(
            model_name='place',
            name='Place_ID',
            field=models.CharField(max_length=6, blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='person',
            name='Person_ID',
            field=models.CharField(max_length=6, blank=True, null=True),
        ),
        migrations.RemoveField(
            model_name='place',
            name='Address',
        ),
        migrations.AddField(
            model_name='place',
            name='Address',
            field=models.ManyToManyField(to='neptune.Person', blank=True, verbose_name='Address Name'),
        ),
    ]
