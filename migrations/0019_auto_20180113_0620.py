# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-01-13 06:20
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job_data_2', '0018_auto_20180113_0620'),
    ]

    operations = [
        migrations.AlterField(
            model_name='freelance',
            name='date',
            field=models.DateField(default=datetime.datetime(2018, 1, 13, 6, 20, 55, 372223)),
        ),
        migrations.AlterField(
            model_name='job_detail',
            name='date',
            field=models.DateField(blank=True, default=datetime.datetime(2018, 1, 13, 6, 20, 55, 373762)),
        ),
    ]
