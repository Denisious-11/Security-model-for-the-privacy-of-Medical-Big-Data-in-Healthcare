# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2022-10-20 09:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('OMBD_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Keys',
            fields=[
                ('u_id', models.IntegerField(primary_key=True, serialize=False)),
                ('public_key', models.CharField(max_length=255)),
                ('private_key', models.CharField(max_length=255)),
            ],
        ),
    ]