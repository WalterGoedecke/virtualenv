# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('classic', '0010_auto_20150921_2205'),
    ]

    operations = [
        migrations.AlterField(
            model_name='calculation',
            name='elevation',
            field=models.CharField(default="None'", verbose_name='Elevation (AMSL)', blank=True, max_length=60, null=True),
        ),
    ]
