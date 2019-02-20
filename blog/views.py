# django 的库
from django.conf import settings
from django.core.paginator import Paginator
from django.shortcuts import render_to_response, get_object_or_404

# 第三方库
import markdown

# 本地库
from read_statistic.utils import read_once # 阅读一次计数方法
from .models import Blog, BlogType
from .utils import blogs_pagination,get_blog_types,get_blog_dates,get_hot_blogs

# Create your views here.
def get_blog_common(request, all_blogs):
    '''
    获取博客信息的公共代码
    :param request:
    :return:
    '''
    # ----------------分页操作---------------
    blogs_in_page, page_range = blogs_pagination(request,all_blogs)
    # ----------------统计分类博客数量---------------
    blog_types = get_blog_types()
    # ----------------统计按月博客数量---------------
    blog_dates_dic = get_blog_dates()
    # ----------------获取热门博客---------------
    hot_blogs = get_hot_blogs()
    context = {}
    context['blogs_in_page'] = blogs_in_page
    context['page_range'] = page_range  # 选取当前页面和邻近的4页作为分页显示
    context['blog_types'] = blog_types  # 统计了博客数量的博客类型
    context['blog_dates'] = blog_dates_dic # 统计了博客数量的按月博客
    context['hot_blogs'] = hot_blogs    # 热门博客
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
