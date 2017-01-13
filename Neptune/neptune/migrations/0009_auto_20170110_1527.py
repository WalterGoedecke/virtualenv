# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('neptune', '0008_auto_20170110_1517'),
    ]

    operations = [
        migrations.RenameField(
            model_name='place',
            old_name='Person_Name',
            new_name='Persons',
        ),
    ]
