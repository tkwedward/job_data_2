# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-06-26 00:29
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job_data_2', '0058_auto_20180625_2339'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Job_detail',
        ),
        migrations.AlterField(
            model_name='freelance',
            name='date',
            field=models.DateField(default=datetime.datetime(2018, 6, 26, 0, 29, 36, 731337)),
        ),
    ]
