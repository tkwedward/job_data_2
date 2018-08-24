#coding:utf-8#-*-
from collections import OrderedDict
import datetime, math, json, re, sys
from itertools import chain
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count, Avg, Max, Min, Q
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.template import RequestContext,Template
from django.template.loader import render_to_string
from django.templatetags.static import static
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404

from django.views.decorators.http import require_POST
from .helper_functions import get_data_list, get_data_from_the_url, get_paginator_link, get_Paginator, statistic
import numpy as np
from .forms import ContactForm, FreelanceForm, Search_Bar_Form
from .models import labor_gov, collected_data, User
from .important_list import TYPES_CHOICES

try:
    reload(sys)
    sys.setdefaultencoding('utf-8')
except:
    pass

# 收集回來資料的 model 和 排除了 working_hours_number = 0 case
"""
data
- collected_data_model = 所有經問卷取得的資料 instance
- labor_gov_model = 除去了所有工時為 NaN 的 case
"""
collected_data_model = collected_data.objects.all()
labor_gov_model = labor_gov.objects.exclude(working_hours_number=None).exclude(working_hours_number='').exclude(week_total_hour=0.0)
category_model=None

# 首頁的view

def JSON_Result(request, submitted_form):
    form = submitted_form
    category_model = labor_gov_model.filter(industry=form['industry'])

    uid =  request.user.social_auth.get(provider='facebook').uid

    # 取得用戶的 object，如果沒有就 create一個新的
    try:
        user = User.objects.get(uid=uid)
    except:
        User.objects.create(uid=uid)
        user = User.objects.get(uid=uid)

    user_post_number = len(collected_data.objects.filter(uid=user))

    # 20 如果 user_post_number 少於5, 就手動加入id
    if user_post_number < 5:
        # 因為經過 pandas 後，id 會變成 null，所以要手動加入 id，這裏的next_id是抽 database 中最後的id
        next_id = collected_data_model.aggregate(maximum=Max('id'))['maximum']+1

        # 30 create 一個新的 post instance
        b = collected_data(
            company='test--'+form['company'], # 公司名稱
            industry=form['industry'], # 行業
            jobTitle=form['jobTitle'], #
            location2=form['location2'],
            salary_type=form['salary_type'],# 工作形態
            job_type=form['salary_type'],# 工作形態
            gender=form['gender'],#性別
            latest_year=form['latest_year'],
            salary=form['salary'],
            contract_week_hour=form['contract_week_hour'],
            year_of_working=form['year'],
            week_total_hour=form['week_total_hour'],
            OT_frequency=form['OT_frequency'],
            OT_payment=form['OT_payment'],
            working_day_number=form['working_day_number'],
            id=next_id,
            uid=user,
            date=datetime.datetime.now().date()
        )
        b.save()
    else:
        # 40 如果多於5 次，就出 error message
        messages.error(request, "你提交資料的次數超過5次")
    """
    傳送的data︰
    時間︰min, max, average
    組別︰category
    """
    salary_classification = []
    salary_step = None
    salary_start_value = None
    salary_color=None
    hour_classification = []
    hour_step = 5
    hour_start_value = 0
    hour_color=None

    if (form['salary_type']==u'月薪'):
        salary_step = 2000
    elif (form['salary_type']==u'日薪'):
        salary_step = 50
    elif (form['salary_type']==u'時薪'):
        salary_step = 10

    # money
    salary_classification = json.dumps(statistic(type='salary', field1='salary', data_list=salary_classification, model=category_model, form=form, step=salary_step))

    # working hour
    hour_classification = json.dumps(statistic(type='week_total_hour', field1='week_total_hour', data_list=hour_classification, model=category_model, form=form, step=hour_step))
    # print(hour_classification)
    # return redirect(about_us)
    return {
        'form': submitted_form,
        'hour_classification':hour_classification,
        'salary_classification':salary_classification,
        'category': submitted_form['industry']}
    # return render(request, 'WKnews_web_draft 3_1.htm', {'form': form, 'type':'normal', "homepage":True, 'json':hour_classification, "show_overlay":True})

def homepage(request):
    """
    data:
        form: 在頁面一開始時的問卷
        cleaned_form: cleaned_form 的session

    return:
        form: 填好了的form 和 type: 'normal'是用來與 freelance的情況做區分
    """

    cleaned_form = request.session.get('cleaned_form', "")

    if cleaned_form:
        print(cleaned_form)
        del request.session['cleaned_form']
        form = ContactForm(initial={
            'company': cleaned_form['company'],
            'industry':cleaned_form['industry'],
            # 職位名稱
            'jobTitle':cleaned_form['jobTitle'],
            # 工作地點
            'place':cleaned_form['location2'],
            # 職務型態
            'job_type':cleaned_form['job_type'],
            #工作天數
            'date_number':cleaned_form['working_day_number'],
            # 性別
            'gender':cleaned_form['gender'],
            # 你最近從事這份工作的年份
            'latest_year':cleaned_form['latest_year'],
            # 支薪周期
            'salary_period':cleaned_form['salary_type'],
            'salary':cleaned_form['salary'],
            # 行業年資
            'year':cleaned_form['year'],
            # 合約列明一周工時
            'contract_hour':cleaned_form['contract_week_hour'],
            # 每周工時
            'week_total_hour':cleaned_form['week_total_hour'],

            # 超時
            'OT_payment':cleaned_form['OT_payment'],

            # 加班補償
            'OT_frequency':cleaned_form['OT_frequency'],
        }) # ContactForm

        # return 的是一個 JsonResponse({ 'form': submitted_form, 'hour_classification':hour_classification, 'salary_classification':salary_classification,'category': submitted_form['industry']} )
        # 現在的問題是在 login 後能夠出到

        # return redirect(added)
        return render(request, 'WKnews_web_draft 3_1.htm', {'form': form, 'type':'normal', "homepage":True, 'click_JSON':True})


    form = ContactForm(
            initial={
            'company': '搵你笨保險有限公司',
            'industry':u'保險',
            # 職位名稱
            'jobTitle':'保險推銷員',
            # 工作地點
            'place':'東區',
            # 職務型態
            'job_type':'全職',
            #工作天數
            'date_number':'10',
            # 性別
            'gender':'f',
            # 你最近從事這份工作的年份
            'latest_year':2015,
            # 支薪周期
            'salary_period':'月薪',
            'salary':'10000',
            # 行業年資
            'year':9,
            # 合約列明一周工時
            'contract_hour':40,
            # 每周工時
            'week_total_hour':40,

            # 超時
            'OT_payment':u'有',

            # 加班補償
            'OT_frequency': u'絕少',
            }
        )

    # homepage: 用來highlight homepage 的 navbar
    return render(request, 'WKnews_web_draft 3_1.htm', {'form': form, 'type':'normal', "homepage":True})

def about_us(request):
    """
    關於我們的頁面
    """
    return render(request, 'about_us.htm', {"about":True})

#功能
"""
type 是從 salary 或 working_hour 二選一
field1是放入由ajax 傳送過來的form中其中的field value，如果是 type 是 salary，這裏的field value會是工時，否則就是none
"""


def afterFacebookLogin(request):
    return redirect("added")


# @require_POST
def added(request):
    """
    data:
        - form = 用戶提交的表格的資籵，入面有︰
            1. salary_type︰月薪、日薪或時薪
        - user_post_number = user所提交的表格總數
        category_model
        - form['agreement'] = 如果用戶同意提交表格，value 是 true
        - uid = 用戶的 facebook id
        - b = 新的 post instance

        # 畫 時薪 用的資料
        - salary_classification = json 化了的時薪 statistic
        - salary_step =
        - salary_start_value = None
        - salary_color=None

        # 畫 工時 用的資料
        - hour_classification = json 化了的工時 statistic
        - hour_step = 5，每5小時為一個 bar
        - hour_start_value = 0, x-axis最細的數值
        - hour_color=None, hour_bar 的顏色，可以是黃色或橙色



    處理用戶提交的表格
    10 如果答應放入資料，就取出該用戶的uid
    20 如果 user_post_number 少於5, 就找出 database 中最大的 id
    30 create 一個新的 post instance
    40 如果多於5 次，就出 error message

    return
    - JsonResponse
        - form︰用戶的表格
        - hour_classification
        - salary_classification
        - category︰行業
    """

    # 10 如果答應放入資料，就取出該用戶的uid
    if not request.user.is_authenticated():
        print("unauthenticated")
        request.session['cleaned_form'] = request.POST.dict()
        # redirect_url = "/oauth/login/facebook/"
        # return redirect("social:begin", "facebook")
        # return HttpResponsePermanentRedirect(redirect_url)
        return JsonResponse({
            'error': 'error',
            'form': None,
            'hour_classification':None,
            'salary_classification':None,
            'category': None
            })
    # 取得用戶的 facebook uid, 如果找不到，代表沒有login，所以轉向 login page
    if request.user.is_authenticated():
        print("authenticated")
        submitted_form = request.session.get('cleaned_form', "")

        if not submitted_form:
             submitted_form = request.POST.dict()
        json_result = JSON_Result(request, submitted_form)
        print(json_result)
        return JsonResponse(json_result)
        # return redirect(homepage)

        # return JsonResponse({
        #     'form': submitted_form,
        #     'hour_classification':hour_classification,
        #     'salary_classification':salary_classification,
        #     'category': submitted_form['industry']}
        #     )

def success(request):
    """
    用來測試提交資料成功的頁面，暫時沒有用
    """
    return HttpResponse('success')

def jobs_gov_data_detail(request, model_name, id):
    """
    在 search page 之中，用來找出某個職位的 詳細資料

    arg:
        request:
        model_name: 選勞工處資料或是問卷收集的資料
        id: 讓 instance 的 id

    data:
    # 畫 graph 的資料
    - salary_classification = 傳送到 html 的 json, 裏面有 bar 的 range, 高度 和 顏色
    - salary_step = 工資的 range
    - salary_start_value = x-axis最細的數值
    - salary_color= bar 的顏色

    # 畫 graph 的資料，同上
    - hour_classification = []
    - hour_step = 5
    - hour_start_value = 0
    - hour_color=None

    - result_file = 將前面的資料 (hour_classification, salary_classification 和 category) wrap 起來傳送到 html

    form = 在 search page 中填寫在 graph 前面的資料，如公司、industry、jobTitle等等資料

    return
    - form
    - hour_classification
    - salary_classification
    - category
    - json_file

    processing:
    10 如果 model 是 collected_data, 就從 database 中取出讓 instance，否則就從 勞工處資料中取出資料
    """
    # 10 如果 model 是 collected_data, 就從 database 中取出讓 instance，否則就從 勞工處資料中取出資料
    if model_name == 'collected_data':
        instance = get_object_or_404(collected_data, id=int(id))
    else:
        instance = get_object_or_404(labor_gov, id=id)

    salary_classification = []
    salary_step = 2000
    salary_start_value = None
    salary_color=None
    hour_classification = []
    hour_step = 5
    hour_start_value = 0
    hour_color=None

    form = {
        'company': instance.company,
        'industry': instance.industry,
        'jobTitle':instance.jobTitle,
        'place': instance.location2,
        'salary_period': instance.salary_type,
        'date_number': instance.working_day_number,
        'week_total_hour': instance.week_total_hour,
        'salary': instance.salary,
    }

    # category_model = labor_gov_model.filter(category=instance.category)
    category_model = labor_gov_model.filter(industry=instance.industry)
    # money
    salary_classification = json.dumps(statistic(type='salary', field1='salary', data_list=salary_classification, model=category_model, form=form, step=salary_step))

    # working hour
    hour_classification = json.dumps(statistic(type='week_total_hour', field1='week_total_hour', data_list=hour_classification, model=category_model, form=form, step=hour_step))

    result_file = {
        'hour_classification':hour_classification,
        'salary_classification':salary_classification,
        'category': form['industry']
        }
    json_file = json.dumps(result_file)

    return render(request, 'analysis.html', {'form': form,
    'hour_classification':hour_classification,
    'salary_classification':salary_classification,
    'category': form['industry'], 'json':json_file, 'search':True, 'page':'detail'})

def jobs_gov_data(request):
    search_form = Search_Bar_Form()
    model_used=labor_gov_model

    position, industry, location, salary_type, upper_limit, lower_limit, data_list_order_by, data_list_sort_by, page, model_name = get_data_from_the_url(request)

    paginator_link = get_paginator_link(position, industry, location, salary_type, upper_limit, lower_limit, data_list_order_by, data_list_sort_by)

    data_list = model_used.exclude(week_total_hour=0.0)

    data_show, show_page_list = get_Paginator(data_list, request, page)

    return render(request, 'search_page3.htm', {'list': data_show, 'form': search_form, 'paginator_link':paginator_link, #'category_list':CATEGORY_CHOICES,
    'show_page_list':show_page_list, 'search':True})

def get_search(request, position="", industry="", location="", salary="", salary_type="", salary_filter="", data_list_order_by="", data_list_sort_by="", page_from_link=1):
    data_list = []
    if request.is_ajax():
        position, industry, location, salary_type, upper_limit, lower_limit, data_list_order_by, data_list_sort_by, page, model_name = get_data_from_the_url(request)

        paginator_link = get_paginator_link(position, industry, location, salary_type, upper_limit, lower_limit, data_list_order_by, data_list_sort_by)

        data_list = get_data_list(position, industry, location, upper_limit, lower_limit, salary_type, data_list_order_by, data_list_sort_by, model_name)

        """paginator"""
        data_show, show_page_list = get_Paginator(data_list, request, page)

        html = render_to_string('data_table.html', {'list': data_show, 'show_page_list':show_page_list, 'paginator_link':paginator_link})
        # print(html)
        return JsonResponse({'html':html})
    else:
        search_form = Search_Bar_Form(request.GET)
        position, industry, location, salary_type, upper_limit, lower_limit, data_list_order_by, data_list_sort_by, page, model_name = get_data_from_the_url(request)

        paginator_link = get_paginator_link(position, industry, location, salary_type, upper_limit, lower_limit, data_list_order_by, data_list_sort_by)

        data_list = get_data_list(position, industry, location, upper_limit, lower_limit, salary_type, data_list_order_by, data_list_sort_by, model_name)

        """paginator"""
        data_show, show_page_list = get_Paginator(data_list, request, page_from_link)
        # print(data_show, show_page_list, data_list)
        return render(request, 'search_page3.htm', {'list': data_show, 'form':search_form, 'paginator_link':paginator_link, 'show_page_list':show_page_list, 'search':True})

def add_json_data(request):
    """
    用來將資料放入資料庫中，現在沒有用
    """
    name_cat = u'生產/工廠職位'

    data = json.load(open('/Users/mac/Desktop/projects/selenium/生產.txt'))

    for x in data:
        try:
            labor_gov.objects.create(
            number=x['number'],
            company=x['company'],
            location=x['location'],
            treatment= x['treatment'],
            date=x['date'],
            responsibility=x['responsibility'],
            industry=x['industry'],
            jobTitle=x['jobTitle'],
            category= name_cat,
            week_total_hour=0
            )
        except:
            print (x)
    return HttpResponse('ok')

def get_name_2(request):
    """
    之後用來做 Freelance 問卷的頁面，暫時並沒有用途
    """
    form = FreelanceForm()
    return render(request, 'name.html', {'form': form, 'type2':'freelance'})

    #第二頁

def Freelance_add(request):
    """
    之後用來做 Freelance 提交問卷時的處理程序，暫時沒有用
    """
    if request.method == "POST":
        form = FreelanceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success')
    else:
        form = FreelanceForm()
    return render(request, 'freelance_form.html', {'form': form})
