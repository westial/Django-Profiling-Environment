# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigIntegerField(max_length=20, serialize=False, primary_key=True)),
                ('title', models.CharField(max_length=90)),
                ('date', models.DateField()),
                ('description', models.TextField()),
                ('image', models.CharField(max_length=255)),
                ('inventory', models.BigIntegerField(max_length=20)),
                ('created', models.DateTimeField()),
                ('modified', models.DateTimeField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Sale',
            fields=[
                ('id', models.BigIntegerField(max_length=20, serialize=False, primary_key=True)),
                ('created', models.DateTimeField()),
                ('product', models.ForeignKey(to='app_rdbms.Product')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigIntegerField(max_length=20, serialize=False, primary_key=True)),
                ('email', models.CharField(max_length=90)),
                ('created', models.DateTimeField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='sale',
            name='user',
            field=models.ForeignKey(to='app_rdbms.User'),
            preserve_default=True,
        ),
    ]
