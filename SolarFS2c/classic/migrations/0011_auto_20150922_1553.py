# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('classic', '0010_auto_20150921_1616'),
    ]

    operations = [
        migrations.AlterField(
            model_name='calculation',
            name='ephem_sequence',
            field=models.TextField(null=True, max_length=6000, blank=True),
        ),
        migrations.AlterField(
            model_name='calculation',
            name='irradiance_sequence',
            field=models.TextField(null=True, max_length=6000, blank=True),
        ),
    ]
