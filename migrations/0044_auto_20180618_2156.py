# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-06-18 21:56
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job_data_2', '0043_auto_20180618_2153'),
    ]

    operations = [
        migrations.RenameField(
            model_name='collected_data',
            old_name='year',
            new_name='year_of_working',
        ),
        migrations.AlterField(
            model_name='freelance',
            name='date',
            field=models.DateField(default=datetime.datetime(2018, 6, 18, 21, 56, 11, 571475)),
        ),
        migrations.AlterField(
            model_name='job_detail',
            name='date',
            field=models.DateField(default=datetime.datetime(2018, 6, 18, 21, 56, 11, 572788)),
        ),
    ]
