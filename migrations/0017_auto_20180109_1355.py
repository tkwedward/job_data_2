# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-01-09 13:55
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job_data_2', '0016_auto_20180109_0912'),
    ]

    operations = [
        migrations.AlterField(
            model_name='freelance',
            name='date',
            field=models.DateField(default=datetime.datetime(2018, 1, 9, 13, 55, 7, 726492)),
        ),
        migrations.AlterField(
            model_name='job_detail',
            name='date',
            field=models.DateField(blank=True, default=datetime.datetime(2018, 1, 9, 13, 55, 7, 727997)),
        ),
    ]
