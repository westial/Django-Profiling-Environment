# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_rdbms', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='created',
            field=models.DateTimeField(auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='product',
            name='modified',
            field=models.DateTimeField(auto_now=True, auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='sale',
            name='created',
            field=models.DateTimeField(auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='user',
            name='created',
            field=models.DateTimeField(auto_now_add=True),
            preserve_default=True,
        ),
    ]
