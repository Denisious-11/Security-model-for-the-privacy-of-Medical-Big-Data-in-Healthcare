# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2022-10-20 10:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('OMBD_app', '0002_keys'),
    ]

    operations = [
        migrations.CreateModel(
            name='Temp_Users',
            fields=[
                ('u_id', models.IntegerField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=255)),
                ('phone', models.CharField(max_length=255)),
                ('email', models.CharField(max_length=255)),
                ('password', models.CharField(max_length=255)),
                ('age', models.CharField(max_length=255)),
                ('gender', models.CharField(max_length=255)),
            ],
        ),
    ]