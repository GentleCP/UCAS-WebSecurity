'''
@project: MyWebSite
@author: GentleCP
@file: urls.py
@time: 2019/1/31 16:12
'''
from django.urls import path
from .import views
urlpatterns = [
    # localhost:8000/blog/
    path('',views.get_blog_list,name = "blog_list"), # blog list
    path('blog_detail/<int:blog_id>',views.get_blog_detail,name = "blog_detail"), # blog详细内容
    path('blog_type/<int:blog_type_id>',views.get_blog_with_type, name = "blog_with_type") #所有该类型下的blog
]
