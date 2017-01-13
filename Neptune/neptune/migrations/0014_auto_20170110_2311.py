# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('neptune', '0013_auto_20170110_2311'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='Places',
            field=models.ManyToManyField(verbose_name='Link to Places', blank=True, to='neptune.Place'),
        ),
    ]
