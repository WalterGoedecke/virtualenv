# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('neptune', '0006_auto_20170110_1503'),
    ]

    operations = [
        migrations.AddField(
            model_name='place',
            name='Person_Name',
            field=models.ManyToManyField(blank=True, verbose_name='Link to Person', to='neptune.Person'),
        ),
        migrations.RemoveField(
            model_name='place',
            name='Address',
        ),
        migrations.AddField(
            model_name='place',
            name='Address',
            field=models.CharField(blank=True, verbose_name='Address Name', max_length=20),
        ),
    ]
