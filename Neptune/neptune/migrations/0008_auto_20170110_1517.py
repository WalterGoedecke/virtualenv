# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('neptune', '0007_auto_20170110_1515'),
    ]

    operations = [
        migrations.AlterField(
            model_name='place',
            name='Address',
            field=models.CharField(max_length=40, blank=True, verbose_name='Address Name'),
        ),
    ]
