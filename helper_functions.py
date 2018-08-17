#coding:utf-8#-*-
import datetime, math, json, re, sys
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count, Avg, Max, Min, Q
from .models import labor_gov, collected_data, User


collected_data_model = collected_data.objects.all()
labor_gov_model = labor_gov.objects.exclude(working_hours_number=None).exclude(working_hours_number='').exclude(week_total_hour=0.0)
category_model=None

def get_data_list(position, industry, location, upper_limit, lower_limit, salary_type, data_list_order_by="", data_list_sort_by="", model_name=""):
    """
    用來處理
    """
    data_list = labor_gov_model
    if model_name=='job_gov_data':
        data_list = labor_gov_model
    elif model_name=='collected_data':
        data_list = collected_data_model.order_by('-id')
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

def statistic(type, field1, data_list, model=None, form=None, step=None):
    print(type, field1, data_list)
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
    model_used = model
    # model_used = model.filter(salary_type='月薪')
    # 這裏的field1是 money或是 week_total_hour
    max_list = model_used.aggregate(maximum=Max(field1))
    mini_list = model_used.aggregate(minimum=Min(field1))

    # 20 找出 instance 的資料
    instance_data = float(form[type])

    # 這30 計算 graph 中的 最大 (range_max)和最小值 (range_min)
    try:
        range_min = int(math.floor(float(mini_list['minimum'])))
    except Exception as e:
        print(e)
        print(mini_list)
        range_min=0
    try:
        range_max = int(math.ceil(float(max_list['maximum'])))
    except Exception as e:
        print(e)
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
    if combine_number:
        if type == 'salary' and len(data_list)>max_bar:
            last_item = '{}以上'.format(int(min(combine_number)))
            data_list.append({'range':last_item, 'number':combine_length, 'color':color})
    return data_list

    # 返回 instance 的資料, 使用了的model，最小值和最大值
