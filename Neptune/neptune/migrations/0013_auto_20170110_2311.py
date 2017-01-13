# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('neptune', '0012_place_compute_gps'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='Places',
            field=models.ManyToManyField(blank=True, verbose_name='Link to Places', to='neptune.Place', null=True),
        ),
    ]
