#coding:utf-8#-*-

from __future__ import unicode_literals

from django.db import models
from django.utils.timezone import datetime
from django.urls import reverse
from .important_list import DISTRICT_LIST, INDUSTRY_LIST, SALARY_TYPE_LIST, SEX_CHOICES, TYPES_CHOICES, OTP_CHOICES, OT_CHOICES

class User(models.Model):
    uid = models.CharField(max_length=100)



# Create your models here.
employed_choices = (('yes','在職'), ('no','無業'))

experience_choices=(('0', '請選擇'), ('1','1年或以下'), ('2','2年或以下'), ('3','3年或以下'))


CHOICES = (('1', 'First',), ('2', 'Second',))


class Freelance(models.Model):
    job_name = models.CharField( max_length=100)
    job_location = models.CharField( max_length=100)
    average = models.IntegerField(default=None)
    max_salary = models.IntegerField(default=None)
    min_salary = models.IntegerField(default=None)
    date = models.DateField(default=datetime.today())

    def __unicode__(self):
        return self.job_name

# 在網上問卷收集來的數據
class collected_data(models.Model):
    time_stamp = models.CharField(max_length=50, blank=True, null=True)
    # 1
    company = models.CharField(max_length=50)

    # 2 即是industry
    industry = models.CharField(max_length=20,choices=INDUSTRY_LIST, blank=True, null=True)
    category = models.CharField(max_length=20,choices=INDUSTRY_LIST, blank=True, null=True)

    # 3
    jobTitle = models.CharField(max_length=50)

    # 4. 地點
    location2 = models.CharField(max_length=50, blank=True)

    # 5. 工作形態
    salary_type = models.CharField(max_length=50, choices=SALARY_TYPE_LIST, blank=True, null=True)
    job_type = models.CharField(max_length=50, choices=TYPES_CHOICES, blank=True, null=True)

    # 6. 每周工作天數
    working_day_number = models.FloatField(blank=True, null=True)

    # 7. 性別
    gender = models.CharField(max_length=5, choices=SEX_CHOICES, null=True)

    # 8. 最近工作年份
    latest_year = models.CharField(blank=True, null=True, max_length=100)

    # 10. 薪金
    salary = models.FloatField(blank=True, null=True)
    salary_text = models.CharField(blank=True, null=True, max_length=100)

    # 11. 年資
    year_of_working = models.CharField(blank=True, null=True, max_length=100)

    # 12. 合約每週工時
    contract_week_hour = models.FloatField(blank=True, null=True)

    # 13. 實際每週工時
    week_total_hour = models.FloatField(blank=True, null=True)

    # 14.
    OT_frequency = models.CharField(max_length=20,choices=OT_CHOICES)

    # 15.
    OT_payment = models.CharField(max_length=50, choices=OTP_CHOICES)

    # 交form的日子
    date = models.CharField(blank=True, null=True, max_length=100)

    email = models.EmailField(blank=True, null=True)

    uid = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)

    working_day_number_float = models.FloatField(blank=True, null=True)
    working_hours_number_float = models.FloatField(blank=True, null=True)

    def __str__(self):
        return self.jobTitle
    def __unicode__(self):
        return self.jobTitle
    def get_absolute_url(self):
        return reverse('jobs_gov_data_detail', kwargs={'model_name': 'collected_data','id':self.id})

# 在勞工處收集的數據
class labor_gov(models.Model):
    number = models.CharField(max_length=50)
    date = models.CharField(max_length=50)
    jobTitle = models.CharField(max_length=50)
    company = models.CharField(max_length=200)
    location = models.CharField(max_length=50)
    industry = models.CharField(max_length=50)
    industry_2 = models.CharField(max_length=50)
    responsibility = models.TextField()
    treatment = models.TextField()
    category = models.CharField(max_length=10, null=True)
    exported = models.BooleanField(default=False)
    salary3 = models.CharField(max_length=50, blank=True)
    salary = models.FloatField(blank=True, null=True)
    salary_type = models.CharField(max_length=10, blank=True)
    working_date = models.CharField(max_length=50, blank=True)
    location2 = models.CharField(max_length=50, blank=True)

    working_week = models.CharField(max_length=50, blank=True)
    working_hours = models.CharField(max_length=50, blank=True)
    working_hours_number = models.CharField(max_length=50, blank=True)
    working_day_number= models.CharField(max_length=50, blank=True)
    working_shift = models.CharField(max_length=50, blank=True)
    working_hours_number_float = models.FloatField(blank=True, null=True)
    working_day_number_float= models.FloatField(blank=True, null=True)

    start_time = models.TextField()

    end_time = models.TextField()

    week_total_hour = models.FloatField(blank=True, null=True)

    def __str__(self):
        return self.jobTitle
    def __unicode__(self):
        return self.jobTitle

    def get_absolute_url(self):
        return reverse('jobs_gov_data_detail', kwargs={'model_name': 'labor_gov','id':self.id})
