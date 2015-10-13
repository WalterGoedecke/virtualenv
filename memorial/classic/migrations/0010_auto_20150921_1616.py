# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('classic', '0009_remove_calculation_ephem_azimuth'),
    ]

    operations = [
        migrations.AlterField(
            model_name='calculation',
            name='elevation',
            field=models.FloatField(null=True, default=0.0, blank=True),
        ),
    ]
