# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-11-25 15:01
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job_data_2', '0010_auto_20171125_1444'),
    ]

    operations = [
        migrations.AddField(
            model_name='labor_gov',
            name='working_hours_number',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='freelance',
            name='date',
            field=models.DateField(default=datetime.datetime(2017, 11, 25, 15, 1, 26, 476975)),
        ),
        migrations.AlterField(
            model_name='job_detail',
            name='date',
            field=models.DateField(blank=True, default=datetime.datetime(2017, 11, 25, 15, 1, 26, 478237)),
        ),
    ]
