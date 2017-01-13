# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('neptune', '0010_auto_20170110_1536'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='place',
            name='Persons',
        ),
        migrations.AddField(
            model_name='person',
            name='Places',
            field=models.ManyToManyField(to='neptune.Place', verbose_name='Link to Places'),
        ),
    ]
