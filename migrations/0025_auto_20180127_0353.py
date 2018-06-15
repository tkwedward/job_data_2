# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-01-27 03:53
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job_data_2', '0024_auto_20180127_0353'),
    ]

    operations = [
        migrations.AlterField(
            model_name='freelance',
            name='date',
            field=models.DateField(default=datetime.datetime(2018, 1, 27, 3, 53, 34, 257803)),
        ),
        migrations.AlterField(
            model_name='job_detail',
            name='date',
            field=models.DateField(blank=True, default=datetime.datetime(2018, 1, 27, 3, 53, 34, 259017)),
        ),
        migrations.AlterField(
            model_name='labor_gov',
            name='money',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]
