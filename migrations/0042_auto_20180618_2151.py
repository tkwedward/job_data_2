# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-06-18 21:51
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job_data_2', '0041_auto_20180618_2149'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collected_data',
            name='date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='freelance',
            name='date',
            field=models.DateField(default=datetime.datetime(2018, 6, 18, 21, 51, 45, 939848)),
        ),
        migrations.AlterField(
            model_name='job_detail',
            name='date',
            field=models.DateField(default=datetime.datetime(2018, 6, 18, 21, 51, 45, 940919)),
        ),
    ]
