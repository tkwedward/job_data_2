# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-06-27 00:33
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job_data_2', '0062_auto_20180627_0019'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collected_data',
            name='year_of_working',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='freelance',
            name='date',
            field=models.DateField(default=datetime.datetime(2018, 6, 27, 0, 33, 16, 838598)),
        ),
    ]
