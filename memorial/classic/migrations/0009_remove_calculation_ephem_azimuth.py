# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('classic', '0008_calculation_ephem_azimuth'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='calculation',
            name='ephem_azimuth',
        ),
    ]
