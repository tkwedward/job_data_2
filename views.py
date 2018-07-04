#coding:utf-8#-*-
from collections import OrderedDict
import datetime, math, json, re, sys
from itertools import chain

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count, Avg, Max, Min, Q
from django.http import HttpResponse, JsonResponse
from django.template import RequestContext,Template
from django.template.loader import render_to_string
from django.templatetags.static import static
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404

from django.views.decorators.http import require_POST

import numpy as np
from .forms import ContactForm, FreelanceForm, Search_Bar_Form
from .models import labor_gov, collected_data, User
from .important_list import TYPES_CHOICES

# reload(sys)
# sys.setdefaultencoding('utf-8')

# 收集回來資料的 model 和 排除了 working_hours_number = 0 case
"""
data
- collected_data_model = 所有經問卷取得的資料 instance
- labor_gov_model = 除去了所有工時為 NaN 的 case
"""
collected_data_model = collected_data.objects.all()
labor_gov_model = labor_gov.objects.exclude(working_hours_number=None).exclude(working_hours_number='').exclude(week_total_hour=0.0)

# 首頁的view
def homepage(request):
    """
    data:
        form: 在頁面一開始時的問卷

    return:
        form: 填好了的form 和 type: 'normal'是用來與 freelance的情況做區分
    """

    form = ContactForm(
        initial={
        # 'company': '搵你笨保險有限公司',
        # 'industry':'政府部門',
        # # 職位名稱
        # 'jobTitle':'保險推銷員',
        # # 工作地點
        # 'place':'東區',
        # # 職務型態
        # 'job_type':'全職',
        # #工作天數
        # 'date_number':'10',
        # # 性別
        # 'gender':'f',
        # # 你最近從事這份工作的年份
        # 'latest_year':2015,
        # # 支薪周期
        # 'salary_period':'月薪',
        # 'salary':'10000',
        # # 行業年資
        # 'year':9,
        # # 合約列明一周工時
        # 'contract_hour':40,
        # # 每周工時
        # 'week_total_hour':40,
        #
        # # 超時
        # 'OT_payment':u'有',
        #
        # # 加班補償
        # 'OT_frequency': u'絕少',

        # week_total_hour = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '一周實際工時'}))

        })

    return render(request, 'WKnews_web_draft 3_1.htm', {'form': form, 'type':'normal'})

def about_us(request):
    """
    關於我們的頁面
    """
    return render(request, 'about_us.htm', {})



#功能
"""
type 是從 salary 或 working_hour 二選一
field1是放入由ajax 傳送過來的form中其中的field value，如果是 type 是 salary，這裏的field value會是工時，否則就是none
"""
category_model=None

def statistic(type, field1, data_list, model=None, form=None, step=None):
    """
    arg:
        type = 是想找 工時() 或是 工資() 的statistic
        field1 = 這裏的field1是 money或是 week_total_hour???
        data_list =
        model = 選擇用 collected_data(問卷收集回來的資料) 或是用 labor_gov_model (勞工處收集來的資料)
        form = 從

    data:
        # 畫 graph 前的準備
        - model_used
        - max_list = 用 aggregate method 取得 工時 或 工資 的 maximum
        - mini_list = 用 aggregate method 取得 工時 或 工資 的 minimum
        - range_min = 找出之後畫出來的 graph 的 minimum 數值
        - range_max = 找出之後畫出來的 graph 的 maximum 數值
        - instance_data = 某一個職位 instance 的資料，即是由用戶提交的問卷資料，或是在 search page 之中選的某個職位

        # graph 的 parameter
        - max_bar = Graph 之中最多可以 show 出幾多條 bar chart
        - step = 想每條 bar 相隔多少，例如 工時 想用5小時來分隔，工資 用每2000元為分隔
        - color = graph bar 的顏色，一是黃色(普通)，另一是橙色(選中的)
        - length = bar 的高度

        # 在 graph 中 show 出的資料
        - combine_lenght = 最後一條 bar 的高度
        - combine_number = 最後一條 bar 的 boundary, 例如是 30k 或以上

    processing:
        10. 如果是 salary 的話，想查的是 時薪、日薪或月薪
        20 找出 instance 的資料
        30 計算 graph 中的 最大和最小值

    return:
        - data_list = 裏面有畫graph 的資料
        {
            'range' = 每條 bar 所包括的 range
            'number' = bar 的高度，即是人數
            'color' = bar 的顏色
        }

    explain:

    """
    # 這裏的field1 是薪金形態

    if type == 'salary':
        # model_used = model.filter(salary_type=form['salary_type'])
        pass
        # model_used = model
    model_used = model.filter(salary_type='月薪')
    # 這裏的field1是 money或是 week_total_hour
    max_list = model_used.aggregate(maximum=Max(field1))
    mini_list = model_used.aggregate(minimum=Min(field1))

    # 20 找出 instance 的資料
    instance_data = float(form[type])

    # 這30 計算 graph 中的 最大 (range_max)和最小值 (range_min)
    try:
        range_min = int(math.floor(float(mini_list['minimum'])))
    except Exception as e:
        print(e, 'error in line 116')
        print(mini_list)
        range_min=0
    try:
        range_max = int(math.ceil(float(max_list['maximum'])))
    except Exception as e:
        print(e, 'error in line 121')
        print(mini_list)
        range_max=50
    global combine_length
    global combine_number
    combine_length = 0
    combine_number = set()
    max_bar = 13
    # the following is for data generation


    for counter ,x in enumerate(range(0, range_max, step)):
        """
            這裏的 x 是 range list 之中的某個數值
        """
        if instance_data>=float(x) and instance_data<float(x+step):
            color = 'RGB(247,147,30)'
        else:
            color = 'RGB(252, 238, 33)'

        if type == 'salary':
            if counter > max_bar:
                """
                如果 counter 是大於 max_bar 的話，就
                x: boundary 的 minimum
                1. 先將數字除 1000 來 scale down 到 個位或十位 數字 (因為是用 10k - 30k 來表示，而 database 中的數字都是 10000 來表示的)
                2. 將 minimum (這裏是 x) 加上 step (即是這個 boundary 的 maximum)
                3. 將 combine_number sort
                """
                combine_number.add(math.floor(x/1000))
                combine_number.add(math.floor((x+step)/1000))
                sorted(combine_number, key=float)
                combine_length+= len(model.filter(salary__gte=float(x)).filter(salary__lt=float(x+step)))
            else:
                length = len(model.filter(salary__gte=float(x)).filter(salary__lt=float(x+step)))
                data_list.append({'range':'{}-{}'.format(int(math.floor(x/1000)), int(math.floor((x+step)/1000))), 'number':length, 'color':color})
        else:
            length = len(model.filter(week_total_hour__gte=float(x-step)).filter(week_total_hour__lt=float(x+step)))
            data_list.append({'range':'{}-{}'.format(x, x+step), 'number':length, 'color':color})

    """
    這裏是處理最後一條 bar，因為它是與之後所有 data 合起來，所以與上面的有區別
    """
    if type == 'salary' and len(data_list)>max_bar:
        last_item = '{}以上'.format(int(min(combine_number)))
        data_list.append({'range':last_item, 'number':combine_length, 'color':color})

    return data_list
    # 返回 instance 的資料, 使用了的model，最小值和最大值



@require_POST
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

    form = request.POST.dict()
    category_model = labor_gov_model.filter(industry=form['industry'])

    # 10 如果答應放入資料，就取出該用戶的uid

    if form['agreement']==u'true':

        if not request.user.is_authenticated():
            # redirect_url = "oauth/login/facebook/"
            return JsonResponse({
                'error': 'error',
                'form': None,
                'hour_classification':None,
                'salary_classification':None,
                'category': None
                })

        # 取得用戶的 facebook uid, 如果找不到，代表沒有login，所以轉向 login page
        if request.user.is_authenticated():
            uid =  request.user.social_auth.get(provider='facebook').uid

            # 取得用戶的 object，如果沒有就 create一個新的
            try:
                user = User.objects.get(uid=uid)
            except:
                User.objects.create(uid=uid)
                user = User.objects.get(uid=uid)

            user_post_number = len(collected_data.objects.filter(uid=user))
            print(user_post_number)

            # 20 如果 user_post_number 少於5, 就手動加入id
            if user_post_number < 5:
                # 因為經過 pandas 後，id 會變成 null，所以要手動加入 id，這裏的next_id是抽 database 中最後的id
                next_id = collected_data_model.aggregate(maximum=Max('id'))['maximum']+1

                # 30 create 一個新的 post instance
                b = collected_data(
                    company=form['company'], # 公司名稱
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
    # print(salary_classification)

    return JsonResponse({
        'form': form,
        'hour_classification':hour_classification,
        'salary_classification':salary_classification,
        'category': form['industry']}
        )

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


    category_model = labor_gov_model.filter(category=instance.category)

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
    # json_file = json.dumps(result_file).replace("\\","").replace("\"[","[").replace("]\"","]")
    # print(json_file)

    return render(request, 'analysis.html', {'form': form,
    'hour_classification':hour_classification,
    'salary_classification':salary_classification,
    'category': form['industry'], 'json':json_file})

# 用來在 search function 之中，找出想要display 出來的data list


def get_data_list(position, industry, location, upper_limit, lower_limit, salary_type, data_list_order_by="", data_list_sort_by="", model_name=""):
    """
    用來處理
    """
    data_list = labor_gov_model
    if model_name=='job_gov_data':
        data_list = labor_gov_model
    elif model_name=='collected_data':
        data_list = collected_data_model
    elif model_name=='both':
        data_list = collected_data_model | labor_gov_model

    if position:
        data_list = data_list.filter(jobTitle__contains=position)
    if industry and industry!='all':
        data_list = data_list.filter(industry=industry)
    if location and location!='all':
        data_list = data_list.filter(location2=location)
    if salary_type:
        data_list = data_list.filter(salary_type=salary_type)
    if upper_limit and lower_limit:
        data_list = data_list.filter(salary__gte=lower_limit).filter(salary__lte=upper_limit)

    # 如果data_list_order_by 是 None, 那麼就set "", 否則就set data_list_order_by
    # input 可以是 []
    data_list_order_by = "" if data_list_order_by is None else data_list_order_by

    # 如果data_list_order_by 是 None, 那麼就set "", 否則就set data_list_order_by
    # input 是 "+/-"
    data_list_sort_by = "" if data_list_sort_by is None else data_list_sort_by

    # 這裏將兩個
    result = data_list_order_by + data_list_sort_by

    if result ==u"":
        pass
    else:
        data_list=data_list.order_by(result)

    return data_list

def get_data_from_the_url(request):
    """
    data:
    - position: 工作名稱
    - industry: 行業
    - location: 地點
    - upper_limit: 最高工資
    - lower_limit: 最低工資
    - salary_type: 時薪、日薪或月薪
    - data_list_order_by: 是想 descending 或是 ascending
    - data_list_sort_by:  根據工時、工資來排序
    - page︰pagination 的第幾頁

    processing:
    - 從 url request 中抽出資料，然後用這些資料傳送到 get_paginator_link，用來放到 paginator 中頁數的url

    return:
    - position, industry, location, salary_type, upper_limit, lower_limit, data_list_order_by, data_list_sort_by, page, model_name
    """
    # print('I am using get_data_from_the_url')
    position = request.GET.get('keyword')
    industry = request.GET.get('industry')
    location = request.GET.get('location')
    upper_limit = request.GET.get('upper_limit')
    lower_limit = request.GET.get('lower_limit')
    salary_type = request.GET.get('salary_type')
    data_list_order_by = request.GET.get('order')
    data_list_sort_by = request.GET.get('type')
    page = request.GET.get('page', 1)
    model_name = request.GET.get('model_name')
    # print(position, industry, location, salary_type, upper_limit, lower_limit, data_list_order_by, data_list_sort_by, page)
    return position, industry, location, salary_type, upper_limit, lower_limit, data_list_order_by, data_list_sort_by, page, model_name

def get_paginator_link(position, industry, location, salary_type, upper_limit, lower_limit, data_list_order_by, data_list_sort_by):

    """
    arg:
    - position: 工作名稱
    - industry: 行業
    - location: 地點
    - upper_limit: 最高工資
    - lower_limit: 最低工資
    - salary_type: 時薪、日薪或月薪
    - data_list_order_by: 是想 descending 或是 ascending
    - data_list_sort_by:  根據工時、工資來排序
    - page︰pagination 的第幾頁

    data:
    - paginator_link: 用來傳送到 paginator 中的 url

    return:
    - paginator 中的 url
    """

    paginator_link = "keyword={}&industry={}&location={}&salary_type={}&upper_limit={}&lower_limit={}&data_list_order_by={}&data_list_sort_by={}".format(position, industry, location, salary_type, upper_limit, lower_limit, data_list_order_by, data_list_sort_by)
    return paginator_link

def get_Paginator(data_list, request, page_from_link=None):
    """
    data
    - paginator (每頁 show 10個 data)
    - page = 當前的頁面
    - number_page_show︰ show 出幾多頁 (10頁)
    - show_page_list︰在 html 中出幾頁的數字
    """
    paginator = Paginator(data_list, 10) # Show 25 contacts per page
    page = page_from_link

    if page is None:
        page = 1
    if paginator.num_pages < 11:
        number_page_show = paginator.num_pages
    else:
        number_page_show = 11
    if int(page)-5 >0 :
        show_page_list = [int(page)+x-5 for x in range(number_page_show)]
    else:
        show_page_list = [1+x for x in range(number_page_show)]
    try:
        data_show = paginator.page(page)
    except PageNotAnInteger:
        data_show = paginator.page(1)
    except EmptyPage:
        data_show = paginator.page(paginator.num_pages)
    return data_show, show_page_list


def jobs_gov_data(request):
    search_form = Search_Bar_Form()
    model_used=labor_gov_model

    position, industry, location, salary_type, upper_limit, lower_limit, data_list_order_by, data_list_sort_by, page, model_name = get_data_from_the_url(request)

    paginator_link = get_paginator_link(position, industry, location, salary_type, upper_limit, lower_limit, data_list_order_by, data_list_sort_by)

    data_list = model_used.exclude(week_total_hour=0.0)

    data_show, show_page_list = get_Paginator(data_list, request, page)



    return render(request, 'search_page.htm', {'list': data_show, 'form': search_form, 'paginator_link':paginator_link, #'category_list':CATEGORY_CHOICES,
    'show_page_list':show_page_list})



def get_search(request, position="", industry="", location="", salary="", salary_type="", salary_filter="", data_list_order_by="", data_list_sort_by="", page_from_link=1):
    data_list = []
    if request.is_ajax():
        print('I am using ajax')
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
        return render(request, 'search_page.htm', {'list': data_show, 'form':search_form, 'paginator_link':paginator_link, 'show_page_list':show_page_list})

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
