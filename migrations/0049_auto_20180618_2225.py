# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-06-18 22:25
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job_data_2', '0048_auto_20180618_2223'),
    ]

    operations = [
        migrations.AlterField(
            model_name='freelance',
            name='date',
            field=models.DateField(default=datetime.datetime(2018, 6, 18, 22, 25, 11, 158519)),
        ),
        migrations.AlterField(
            model_name='job_detail',
            name='date',
            field=models.DateField(default=datetime.datetime(2018, 6, 18, 22, 25, 11, 159761)),
        ),
    ]
