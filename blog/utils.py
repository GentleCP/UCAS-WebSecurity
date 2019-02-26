# django库
from django.conf import settings
from django.core.paginator import Paginator
from django.contrib.contenttypes.models import ContentType

# 本地库
from read_statistic.models import ReadNum
from .models import Blog, BlogType

def blogs_pagination(request, all_blogs):
    '''
    博客分页的操作
    :param request:
    :param all_blogs: 所有的博客
    :return: 分页后的博客和页面range
    '''
    blog_paginator = Paginator(all_blogs, settings.BLOGS_PER_PAGE)  # 博客分页器，5条一页
    page_num = request.GET.get('page', 1)  # 获取url请求中页面的参数
    blogs_in_page = blog_paginator.get_page(page_num)  # 根据页面获取到该页的blog对象
    current_page_num = blogs_in_page.number  # 当前页面
    page_range = [i for i in [current_page_num - 2, current_page_num - 1, current_page_num,
                              current_page_num + 1, current_page_num + 2] if
                  i > 0 and i <= blog_paginator.num_pages]
    return blogs_in_page, page_range

def get_blog_types():
    '''
    获取统计了数量的博客类型
    :return: blog_types list
    '''
    blog_types = BlogType.objects.all()
    for blog_type in blog_types:
        blog_count = Blog.objects.filter(blog_type=blog_type).count()  # 根据博客类型统计该类型下的博客数量
        blog_type.blog_count = blog_count
    return blog_types

def get_blog_dates():
    '''
    获取按月统计了数量的博客
    :return:
    '''
    blog_dates = Blog.objects.dates('created_time', 'month', order='DESC')  # 按月份返回博客,是个dates对象
    blog_dates_dic = {}
    for blog_date in blog_dates:
        blog_count = Blog.objects.filter(created_time__year=blog_date.year,
                                         created_time__month=blog_date.month).count()  # 根据取到的月份博客的年月属性挑出博客
        blog_dates_dic[blog_date] = blog_count
    return blog_dates_dic

def get_hot_blogs():
    '''
    获取热门文章，根据阅读量的多少，
    :param obj: model或者是object对象
    :return: 热门文章的list
    '''
    hot_blogs = []
    ct = ContentType.objects.get_for_model(Blog)
    readnums = ReadNum.objects.filter(content_type=ct).order_by('-read_num')  # 暗转阅读量获取
    num_of_hot_blogs = readnums.count()  # 总的已读文章数
    for i in range(num_of_hot_blogs if num_of_hot_blogs < settings.NUM_OF_HOT_BLOGS else settings.NUM_OF_HOT_BLOGS):
        # 如果被阅读博客总数大于最大热门博客显示数量则按最大数量显示
        hot_blog = Blog.objects.get(id=readnums[i].object_id)
        hot_blogs.append(hot_blog)
    return hot_blogs
