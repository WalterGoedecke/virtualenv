# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('classic', '0007_auto_20150909_1235'),
    ]

    operations = [
        migrations.AddField(
            model_name='calculation',
            name='ephem_azimuth',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
