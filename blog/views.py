from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.conf import settings

from .models import Blog, BlogType


# Create your views here.

def get_blog_list(request):
    '''
    获取博客列表，传到前端
    :param request: 前端的request请求
    :return:
    '''
    all_blogs = Blog.objects.all()  # 获取所有的blog

    blog_paginator = Paginator(all_blogs, settings.BLOGS_PER_PAGE)  # 博客分页器，5条一页
    page_num = request.GET.get('page', 1)  # 获取url请求中页面的参数
    blogs_in_page = blog_paginator.get_page(page_num)  # 根据页面获取到该页的blog对象
    current_page_num = blogs_in_page.number  # 当前页面
    page_range = [i for i in [current_page_num - 2, current_page_num - 1, current_page_num,
                                   current_page_num + 1, current_page_num + 2] if
                  i > 0 and i <= blog_paginator.num_pages]
    context = {}
    context['blogs_in_page'] = blogs_in_page
    context['page_range'] = page_range # 选取当前页面和邻近的4页作为分页显示
    context['blog_types'] = BlogType.objects.all()

    return render(request, 'blog_list.html', context)


def get_blog_detail(request, blog_id):
    context = {}
    current_blog = Blog.objects.get(id=blog_id)
    context['previous_blog'] = Blog.objects.filter(created_time__gt=current_blog.created_time).last()
    # 因为按照时间顺序，时间新的排在前面，日期比他大排在他前面，所以取比他大的最后一篇，下面取第一篇同理
    context['next_blog'] = Blog.objects.filter(created_time__lt=current_blog.created_time).first()
    context['blog'] = current_blog
    return render(request, 'blog_detail.html', context)


def get_blog_with_type(request, blog_type_id):
    type = get_object_or_404(BlogType, id=blog_type_id)
    all_blogs = Blog.objects.filter(blog_type=type)  # 获取该type下所有的blog
    # ------------下面是与get_blog_list的公共部分---------------
    blog_paginator = Paginator(all_blogs, settings.BLOGS_PER_PAGE)  # 博客分页器，5条一页
    page_num = request.GET.get('page', 1)  # 获取url请求中页面的参数
    blogs_in_page = blog_paginator.get_page(page_num)  # 根据页面获取到该页的blog对象
    current_page_num = blogs_in_page.number  # 当前页面
    page_range = [i for i in [current_page_num - 2, current_page_num - 1, current_page_num,
                              current_page_num + 1, current_page_num + 2] if
                  i > 0 and i <= blog_paginator.num_pages]
    context = {}
    context['blogs_in_page'] = blogs_in_page
    context['page_range'] = page_range  # 选取当前页面和邻近的4页作为分页显示
    context['blog_types'] = BlogType.objects.all()
    # -------------上面是与get_blog_list的公共部分--------------
    context['blog_type'] = type

    return render(request, 'blog_with_type.html', context)
