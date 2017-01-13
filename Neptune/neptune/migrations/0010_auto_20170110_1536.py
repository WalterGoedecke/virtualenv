# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('neptune', '0009_auto_20170110_1527'),
    ]

    operations = [
        migrations.AlterField(
            model_name='place',
            name='Persons',
            field=models.ManyToManyField(verbose_name='Link to Person', to='neptune.Person'),
        ),
    ]
