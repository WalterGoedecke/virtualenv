# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('neptune', '0011_auto_20170110_1543'),
    ]

    operations = [
        migrations.AddField(
            model_name='place',
            name='Compute_GPS',
            field=models.BooleanField(default=True, verbose_name='Allow geocoder to compute GPS coordinates from Address'),
        ),
    ]
