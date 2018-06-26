# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-06-25 23:29
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job_data_2', '0053_auto_20180619_0108'),
    ]

    operations = [
        migrations.AddField(
            model_name='job_detail',
            name='working_day_number_float',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='freelance',
            name='date',
            field=models.DateField(default=datetime.datetime(2018, 6, 25, 23, 29, 20, 147181)),
        ),
        migrations.AlterField(
            model_name='job_detail',
            name='date',
            field=models.DateField(default=datetime.datetime(2018, 6, 25, 23, 29, 20, 148312)),
        ),
    ]
