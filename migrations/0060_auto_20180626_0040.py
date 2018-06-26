# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-06-26 00:40
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job_data_2', '0059_auto_20180626_0029'),
    ]

    operations = [
        migrations.AlterField(
            model_name='freelance',
            name='date',
            field=models.DateField(default=datetime.datetime(2018, 6, 26, 0, 40, 1, 888538)),
        ),
        migrations.AlterField(
            model_name='labor_gov',
            name='week_total_hour',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
