# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('neptune', '0014_auto_20170110_2311'),
    ]

    operations = [
        migrations.CreateModel(
            name='New_Place',
            fields=[
                ('Place_ID', models.AutoField(serialize=False, primary_key=True)),
                ('Address', models.CharField(max_length=40, blank=True, verbose_name='Address Name')),
                ('Latitude', models.CharField(null=True, blank=True, max_length=16, verbose_name='GPS Latitude - leave blank')),
                ('Longitude', models.CharField(null=True, blank=True, max_length=16, verbose_name='GPS Longitude - leave blank')),
                ('Compute_GPS', models.BooleanField(default=True, verbose_name='Allow geocoder to compute GPS coordinates from Address')),
            ],
        ),
        migrations.AlterField(
            model_name='person',
            name='Person_ID',
            field=models.CharField(null=True, blank=True, max_length=6, verbose_name='Person ID - leave blank'),
        ),
        migrations.AlterField(
            model_name='place',
            name='Place_ID',
            field=models.CharField(null=True, blank=True, max_length=6, verbose_name='Place ID - leave blank'),
        ),
    ]
