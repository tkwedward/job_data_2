#coding:utf-8#-*-

from django.conf.urls import url
from .views import homepage, get_name_2, added,  Freelance_add, jobs_gov_data, jobs_gov_data_detail, add_json_data, get_search, success, about_us, afterFacebookLogin


urlpatterns = [
    url(r'^about_us$', about_us, name="about_us"),

    #第一頁︰用來給人填資料
    url(r'^$', homepage, name="form"),
    url(r'^form/freelance$', get_name_2, name="freelance_form"),

    #第二頁︰用來給人看資料

    # 功能
    url(r'^added$', added, name="added"),
    url(r'^afterFacebookLogin$', afterFacebookLogin, name="afterFacebookLogin"),
    url(r'^success$', success, name="success"),

    url(r'^freelance_added$', Freelance_add, name="freelance_added"),
    # url(r'^search/*', search, name="search"),
    url(r'^search/*', get_search, name="search"),


    # show jobs
    url(r'^data$', jobs_gov_data, name="jobs_gov_data"),
    # url(r'^add_json_data$', add_json_data, name="add_json_data"),

    # analysis.html
    url(r'^jobs_gov_data/(?P<model_name>\w+)/(?P<id>\d+)/$', jobs_gov_data_detail, name="jobs_gov_data_detail"),

]
