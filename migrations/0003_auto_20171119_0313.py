# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-11-19 03:13
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job_data_2', '0002_auto_20171119_0300'),
    ]

    operations = [
        migrations.AddField(
            model_name='labor_gov',
            name='location2',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='freelance',
            name='date',
            field=models.DateField(default=datetime.datetime(2017, 11, 19, 3, 13, 3, 71297)),
        ),
        migrations.AlterField(
            model_name='job_detail',
            name='date',
            field=models.DateField(blank=True, default=datetime.datetime(2017, 11, 19, 3, 13, 3, 72565)),
        ),
    ]
