# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('classic', '0013_auto_20150928_0925'),
    ]

    operations = [
        migrations.AlterField(
            model_name='calculation',
            name='begin',
            field=models.CharField(max_length=30, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='holiday',
            name='holiday_date',
            field=models.DateField(max_length=30, null=True, blank=True),
        ),
    ]
