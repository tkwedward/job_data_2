# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-08-10 16:56
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job_data_2', '0065_auto_20180627_0038'),
    ]

    operations = [
        migrations.AddField(
            model_name='labor_gov',
            name='industry_2',
            field=models.CharField(default='', max_length=50),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='collected_data',
            name='OT_frequency',
            field=models.CharField(choices=[('all', '加班情況'), ('絕少', '絕少'), ('偶爾', '偶爾'), ('經常', '經常'), ('幾乎每天', '幾乎每天')], max_length=20),
        ),
        migrations.AlterField(
            model_name='collected_data',
            name='OT_payment',
            field=models.CharField(choices=[('all', '加班補償'), ('有', '有'), ('沒有', '沒有'), ('不知道', '不知道')], max_length=50),
        ),
        migrations.AlterField(
            model_name='collected_data',
            name='category',
            field=models.CharField(blank=True, choices=[('', '行業'), ('商用服務業', '商用服務業'), ('飲食業', '飲食業'), ('通訊業', '通訊業'), ('建造業', '建造業'), ('住戶服務業', '住戶服務業'), ('教育服務業', '教育服務業'), ('金融業', '金融業'), ('政府部門', '政府部門'), ('醫院', '醫院'), ('酒店業', '酒店業'), ('進出口貿易', '進出口貿易'), ('保險業', '保險業'), ('電子製品業', '電子製品業'), ('金屬製品業', '金屬製品業'), ('塑膠製品業', '塑膠製品業'), ('紡織業', '紡織業'), ('服裝製品業', '服裝製品業'), ('地產業', '地產業'), ('零售業', '零售業'), ('倉庫業', '倉庫業'), ('運輸業', '運輸業'), ('福利機構', '福利機構'), ('批發業', '批發業'), ('其他社區及社會服務業', '其他社區及社會服務業'), ('其他製造業', '其他製造業'), ('其他個人服務業', '其他個人服務業')], max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='collected_data',
            name='gender',
            field=models.CharField(choices=[('', '性別'), ('m', '男'), ('f', '女'), ('other', '其他')], max_length=5),
        ),
        migrations.AlterField(
            model_name='collected_data',
            name='industry',
            field=models.CharField(blank=True, choices=[('', '行業'), ('商用服務業', '商用服務業'), ('飲食業', '飲食業'), ('通訊業', '通訊業'), ('建造業', '建造業'), ('住戶服務業', '住戶服務業'), ('教育服務業', '教育服務業'), ('金融業', '金融業'), ('政府部門', '政府部門'), ('醫院', '醫院'), ('酒店業', '酒店業'), ('進出口貿易', '進出口貿易'), ('保險業', '保險業'), ('電子製品業', '電子製品業'), ('金屬製品業', '金屬製品業'), ('塑膠製品業', '塑膠製品業'), ('紡織業', '紡織業'), ('服裝製品業', '服裝製品業'), ('地產業', '地產業'), ('零售業', '零售業'), ('倉庫業', '倉庫業'), ('運輸業', '運輸業'), ('福利機構', '福利機構'), ('批發業', '批發業'), ('其他社區及社會服務業', '其他社區及社會服務業'), ('其他製造業', '其他製造業'), ('其他個人服務業', '其他個人服務業')], max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='collected_data',
            name='job_type',
            field=models.CharField(blank=True, choices=[('', '職務型態'), ('全職', '全職'), ('兼職(含打工)', '兼職(含打工)'), ('實習', '實習'), ('臨時工', '臨時工'), ('約聘雇', '約聘雇'), ('派遣', '派遣')], max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='collected_data',
            name='salary_type',
            field=models.CharField(blank=True, choices=[('', '支薪周期'), ('月薪', '月薪'), ('半月薪', '半月薪'), ('週薪', '週薪'), ('日薪', '日薪'), ('時薪', '時薪'), ('件薪', '件薪')], max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='freelance',
            name='date',
            field=models.DateField(default=datetime.datetime(2018, 8, 10, 16, 56, 38, 370809)),
        ),
    ]
