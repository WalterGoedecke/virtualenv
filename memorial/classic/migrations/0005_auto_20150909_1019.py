# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('classic', '0004_auto_20150904_2056'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='calculation',
            name='A',
        ),
        migrations.RemoveField(
            model_name='calculation',
            name='B',
        ),
        migrations.AddField(
            model_name='calculation',
            name='address',
            field=models.TextField(null=True, max_length=120, verbose_name='Address', blank=True),
        ),
        migrations.AddField(
            model_name='calculation',
            name='address_slug',
            field=models.SlugField(null=True, blank=True, max_length=120),
        ),
        migrations.AddField(
            model_name='calculation',
            name='begin',
            field=models.CharField(null=True, max_length=30, default='2015, 7, 1, 11', blank=True),
        ),
        migrations.AddField(
            model_name='calculation',
            name='coordinates',
            field=models.CharField(null=True, max_length=80, verbose_name='latitude, longitude', blank=True),
        ),
        migrations.AddField(
            model_name='calculation',
            name='elevation',
            field=models.CharField(null=True, max_length=60, default="None'", verbose_name='Elevation (AMSL)', blank=True),
        ),
        migrations.AddField(
            model_name='calculation',
            name='end',
            field=models.CharField(null=True, max_length=30, default='2015, 7, 1, 12', blank=True),
        ),
        migrations.AddField(
            model_name='calculation',
            name='ephem_sequence',
            field=models.TextField(null=True, max_length=600, blank=True),
        ),
        migrations.AddField(
            model_name='calculation',
            name='formatted_address',
            field=models.TextField(null=True, max_length=120, blank=True),
        ),
        migrations.AddField(
            model_name='calculation',
            name='frequency',
            field=models.CharField(null=True, max_length=20, default='3Min', blank=True),
        ),
        migrations.AddField(
            model_name='calculation',
            name='irradiance_sequence',
            field=models.TextField(null=True, max_length=600, blank=True),
        ),
        migrations.AddField(
            model_name='calculation',
            name='panel_azimuth',
            field=models.FloatField(null=True, max_length=20, default=180, verbose_name='Panel azimuth (degrees from north)', blank=True),
        ),
        migrations.AddField(
            model_name='calculation',
            name='panel_tilt',
            field=models.FloatField(null=True, max_length=20, default=30, verbose_name='Panel tilt (degrees from vertical)', blank=True),
        ),
        migrations.AddField(
            model_name='calculation',
            name='statistics',
            field=models.TextField(null=True, max_length=300, blank=True),
        ),
        migrations.AddField(
            model_name='calculation',
            name='time_sequence',
            field=models.TextField(null=True, max_length=600, blank=True),
        ),
    ]
