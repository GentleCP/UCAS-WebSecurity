# django 的库
from django.conf import settings
from django.core.paginator import Paginator
from django.shortcuts import render_to_response, get_object_or_404

# 第三方库
import markdown

# 本地库
from .models import Blog, BlogType
from read_statistic.utils import read_once # 阅读一次计数方法

# Create your views here.
def get_blog_common(request, all_blogs):
    '''
    获取博客信息的公共代码
    :param request:
    :return:
    '''
    # ----------------分页操作---------------
    blog_paginator = Paginator(all_blogs, settings.BLOGS_PER_PAGE)  # 博客分页器，5条一页
    page_num = request.GET.get('page', 1)  # 获取url请求中页面的参数
    blogs_in_page = blog_paginator.get_page(page_num)  # 根据页面获取到该页的blog对象
    current_page_num = blogs_in_page.number  # 当前页面
    page_range = [i for i in [current_page_num - 2, current_page_num - 1, current_page_num,
                              current_page_num + 1, current_page_num + 2] if
                  i > 0 and i <= blog_paginator.num_pages]
    # ----------------统计分类博客数量---------------
    blog_types = BlogType.objects.all()
    for blog_type in blog_types:
        blog_count = Blog.objects.filter(blog_type=blog_type).count()  # 根据博客类型统计该类型下的博客数量
        blog_type.blog_count = blog_count
    # ----------------统计按月博客数量---------------
    blog_dates = Blog.objects.dates('created_time', 'month', order='DESC')  # 按月份返回博客,是个dates对象
    blog_dates_dic = {}
    for blog_date in blog_dates:
        blog_count = Blog.objects.filter(created_time__year=blog_date.year,
                                         created_time__month=blog_date.month).count()#根据取到的月份博客的年月属性挑出博客
        blog_dates_dic[blog_date] = blog_count

    context = {}
    context['blogs_in_page'] = blogs_in_page
    context['page_range'] = page_range  # 选取当前页面和邻近的4页作为分页显示
    context['blog_types'] = blog_types  # 统计了博客数量的博客类型
    context['blog_dates'] = blog_dates_dic # 统计了博客数量的按月博客
    return context

def get_blog_list(request):
    '''
    获取博客列表，传到前端
    :param request: 前端的request请求
    :return:
    '''
    all_blogs = Blog.objects.all()  # 获取所有的blog
    context = get_blog_common(request, all_blogs)  # 调用公共代码函数，返回context
    return render_to_response('blog_list.html', context)

def get_blog_with_type(request, blog_type_id):
    '''
    按类型获取博客
    :param request:
    :param blog_type_id: 博客类型id
    :return:
    '''
    type = get_object_or_404(BlogType, id=blog_type_id)
    all_blogs = Blog.objects.filter(blog_type=type)  # 获取该type下所有的blog
    # ------------下面是与get_blog_list的公共部分---------------
    context = get_blog_common(request, all_blogs)
    # -------------上面是与get_blog_list的公共部分--------------
    context['blog_type'] = type
    return render_to_response('blog_with_type.html', context)

def get_blog_with_date(request, year, month):
    '''
    按月份获取博客
    :param request:
    :param year:
    :param month:
    :return:
    '''
    all_blogs = Blog.objects.filter(created_time__year=year, created_time__month=month)  # 获取该year,month下所有的blog
    # ------------下面是与get_blog_list的公共部分---------------
    context = get_blog_common(request, all_blogs)
    # -------------上面是与get_blog_list的公共部分--------------
    context['blog_date'] = "%s年%s月" % (year, month)
    return render_to_response('blog_with_date.html', context)

def get_blog_detail(request, blog_id):
    '''
    获取博客完整内容
    :param request:
    :param blog_id: 博客id
    :return:
    '''
    current_blog = Blog.objects.get(id=blog_id)
    read_key = read_once(request,current_blog)
    context = {}
    context['previous_blog'] = Blog.objects.filter(created_time__gt=current_blog.created_time).last()
    # 因为按照时间顺序，时间新的排在前面，日期比他大排在他前面，所以取比他大的最后一篇，下面取第一篇同理
    context['next_blog'] = Blog.objects.filter(created_time__lt=current_blog.created_time).first()
    context['blog'] = current_blog
    # 将blog的内容部分用markdown渲染
    context['blog'].content = markdown.markdown(context['blog'].content,
                                                extensions = [ # 额外参数，用于添加其他额外效果
                                                    'markdown.extensions.extra', # 额外拓展
                                                    'markdown.extensions.codehilite', # 语法高亮拓展
                                                    'markdown.extensions.toc', # 内容表拓展,允许生成目录
                                                ])
    response = render_to_response('blog_detail.html', context)
    response.set_cookie(read_key ,'true') # 设置cookie
    return response
