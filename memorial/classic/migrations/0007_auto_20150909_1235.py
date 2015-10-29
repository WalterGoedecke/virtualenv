# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('classic', '0006_calculation_doc'),
    ]

    operations = [
        migrations.AddField(
            model_name='calculation',
            name='pix1',
            field=models.CharField(null=True, max_length=80, blank=True),
        ),
        migrations.AddField(
            model_name='calculation',
            name='pix2',
            field=models.CharField(null=True, max_length=80, blank=True),
        ),
    ]
