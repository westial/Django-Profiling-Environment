# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_rdbms', '0003_auto_20141217_1301'),
    ]

    operations = [
        migrations.AddField(
            model_name='sale',
            name='quantity',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
