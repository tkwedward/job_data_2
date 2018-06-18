# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-06-18 21:49
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job_data_2', '0040_auto_20180607_0938'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='collected_data',
            name='salary_period',
        ),
        migrations.AddField(
            model_name='collected_data',
            name='industry',
            field=models.CharField(blank=True, choices=[(b'', b'\xe8\xa1\x8c\xe6\xa5\xad'), ('\u5546\u7528\u670d\u52d9\u696d', b'\xe5\x95\x86\xe7\x94\xa8\xe6\x9c\x8d\xe5\x8b\x99\xe6\xa5\xad'), ('\u98f2\u98df\u696d', b'\xe9\xa3\xb2\xe9\xa3\x9f\xe6\xa5\xad'), ('\u901a\u8a0a\u696d', b'\xe9\x80\x9a\xe8\xa8\x8a\xe6\xa5\xad'), ('\u5efa\u9020\u696d', b'\xe5\xbb\xba\xe9\x80\xa0\xe6\xa5\xad'), ('\u4f4f\u6236\u670d\u52d9\u696d', b'\xe4\xbd\x8f\xe6\x88\xb6\xe6\x9c\x8d\xe5\x8b\x99\xe6\xa5\xad'), ('\u6559\u80b2\u670d\u52d9\u696d', b'\xe6\x95\x99\xe8\x82\xb2\xe6\x9c\x8d\xe5\x8b\x99\xe6\xa5\xad'), ('\u91d1\u878d\u696d', b'\xe9\x87\x91\xe8\x9e\x8d\xe6\xa5\xad'), ('\u653f\u5e9c\u90e8\u9580', b'\xe6\x94\xbf\xe5\xba\x9c\xe9\x83\xa8\xe9\x96\x80'), ('\u91ab\u9662', b'\xe9\x86\xab\xe9\x99\xa2'), ('\u9152\u5e97\u696d', b'\xe9\x85\x92\xe5\xba\x97\xe6\xa5\xad'), ('\u9032\u51fa\u53e3\u8cbf\u6613', b'\xe9\x80\xb2\xe5\x87\xba\xe5\x8f\xa3\xe8\xb2\xbf\xe6\x98\x93'), ('\u4fdd\u96aa\u696d', b'\xe4\xbf\x9d\xe9\x9a\xaa\xe6\xa5\xad'), ('\u96fb\u5b50\u88fd\u54c1\u696d', b'\xe9\x9b\xbb\xe5\xad\x90\xe8\xa3\xbd\xe5\x93\x81\xe6\xa5\xad'), ('\u91d1\u5c6c\u88fd\u54c1\u696d', b'\xe9\x87\x91\xe5\xb1\xac\xe8\xa3\xbd\xe5\x93\x81\xe6\xa5\xad'), ('\u5851\u81a0\u88fd\u54c1\u696d', b'\xe5\xa1\x91\xe8\x86\xa0\xe8\xa3\xbd\xe5\x93\x81\xe6\xa5\xad'), ('\u7d21\u7e54\u696d', b'\xe7\xb4\xa1\xe7\xb9\x94\xe6\xa5\xad'), ('\u670d\u88dd\u88fd\u54c1\u696d', b'\xe6\x9c\x8d\xe8\xa3\x9d\xe8\xa3\xbd\xe5\x93\x81\xe6\xa5\xad'), ('\u5730\u7522\u696d', b'\xe5\x9c\xb0\xe7\x94\xa2\xe6\xa5\xad'), ('\u96f6\u552e\u696d', b'\xe9\x9b\xb6\xe5\x94\xae\xe6\xa5\xad'), ('\u5009\u5eab\u696d', b'\xe5\x80\x89\xe5\xba\xab\xe6\xa5\xad'), ('\u904b\u8f38\u696d', b'\xe9\x81\x8b\xe8\xbc\xb8\xe6\xa5\xad'), ('\u798f\u5229\u6a5f\u69cb', b'\xe7\xa6\x8f\xe5\x88\xa9\xe6\xa9\x9f\xe6\xa7\x8b'), ('\u6279\u767c\u696d', b'\xe6\x89\xb9\xe7\x99\xbc\xe6\xa5\xad'), ('\u5176\u4ed6\u793e\u5340\u53ca\u793e\u6703\u670d\u52d9\u696d', b'\xe5\x85\xb6\xe4\xbb\x96\xe7\xa4\xbe\xe5\x8d\x80\xe5\x8f\x8a\xe7\xa4\xbe\xe6\x9c\x83\xe6\x9c\x8d\xe5\x8b\x99\xe6\xa5\xad'), ('\u5176\u4ed6\u88fd\u9020\u696d', b'\xe5\x85\xb6\xe4\xbb\x96\xe8\xa3\xbd\xe9\x80\xa0\xe6\xa5\xad'), ('\u5176\u4ed6\u500b\u4eba\u670d\u52d9\u696d', b'\xe5\x85\xb6\xe4\xbb\x96\xe5\x80\x8b\xe4\xba\xba\xe6\x9c\x8d\xe5\x8b\x99\xe6\xa5\xad')], max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='collected_data',
            name='salary_type',
            field=models.CharField(blank=True, choices=[(b'', b'\xe6\x94\xaf\xe8\x96\xaa\xe5\x91\xa8\xe6\x9c\x9f'), ('\u6708\u85aa', b'\xe6\x9c\x88\xe8\x96\xaa'), ('\u534a\u6708\u85aa', b'\xe5\x8d\x8a\xe6\x9c\x88\xe8\x96\xaa'), ('\u9031\u85aa', b'\xe9\x80\xb1\xe8\x96\xaa'), ('\u65e5\u85aa', b'\xe6\x97\xa5\xe8\x96\xaa'), ('\u6642\u85aa', b'\xe6\x99\x82\xe8\x96\xaa'), ('\u4ef6\u85aa', b'\xe4\xbb\xb6\xe8\x96\xaa')], max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='collected_data',
            name='working_day_number',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='collected_data',
            name='OT_frequency',
            field=models.CharField(choices=[(b'all', b'\xe5\x8a\xa0\xe7\x8f\xad\xe6\x83\x85\xe6\xb3\x81'), ('\u7d55\u5c11', b'\xe7\xb5\x95\xe5\xb0\x91'), ('\u5076\u723e', b'\xe5\x81\xb6\xe7\x88\xbe'), ('\u7d93\u5e38', b'\xe7\xb6\x93\xe5\xb8\xb8'), ('\u5e7e\u4e4e\u6bcf\u5929', b'\xe5\xb9\xbe\xe4\xb9\x8e\xe6\xaf\x8f\xe5\xa4\xa9')], max_length=20),
        ),
        migrations.AlterField(
            model_name='collected_data',
            name='OT_payment',
            field=models.CharField(choices=[(b'all', b'\xe5\x8a\xa0\xe7\x8f\xad\xe8\xa3\x9c\xe5\x84\x9f'), ('\u6709', b'\xe6\x9c\x89'), ('\u6c92\u6709', b'\xe6\xb2\x92\xe6\x9c\x89'), ('\u4e0d\u77e5\u9053', b'\xe4\xb8\x8d\xe7\x9f\xa5\xe9\x81\x93')], max_length=50),
        ),
        migrations.AlterField(
            model_name='collected_data',
            name='date',
            field=models.DateField(default=datetime.datetime(2018, 6, 18, 21, 48, 59, 588031)),
        ),
        migrations.AlterField(
            model_name='collected_data',
            name='gender',
            field=models.CharField(choices=[(b'', b'\xe6\x80\xa7\xe5\x88\xa5'), (b'm', b'\xe7\x94\xb7'), (b'f', b'\xe5\xa5\xb3'), (b'other', b'\xe5\x85\xb6\xe4\xbb\x96')], max_length=5),
        ),
        migrations.AlterField(
            model_name='collected_data',
            name='job_type',
            field=models.CharField(blank=True, choices=[(b'', b'\xe8\x81\xb7\xe5\x8b\x99\xe5\x9e\x8b\xe6\x85\x8b'), ('\u5168\u8077', b'\xe5\x85\xa8\xe8\x81\xb7'), ('\u517c\u8077(\u542b\u6253\u5de5)', b'\xe5\x85\xbc\xe8\x81\xb7(\xe5\x90\xab\xe6\x89\x93\xe5\xb7\xa5)'), ('\u5be6\u7fd2', b'\xe5\xaf\xa6\xe7\xbf\x92'), ('\u81e8\u6642\u5de5', b'\xe8\x87\xa8\xe6\x99\x82\xe5\xb7\xa5'), ('\u7d04\u8058\u96c7', b'\xe7\xb4\x84\xe8\x81\x98\xe9\x9b\x87'), ('\u6d3e\u9063', b'\xe6\xb4\xbe\xe9\x81\xa3')], max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='freelance',
            name='date',
            field=models.DateField(default=datetime.datetime(2018, 6, 18, 21, 48, 59, 584954)),
        ),
        migrations.AlterField(
            model_name='job_detail',
            name='date',
            field=models.DateField(default=datetime.datetime(2018, 6, 18, 21, 48, 59, 586114)),
        ),
    ]
