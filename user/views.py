from django.shortcuts import render,redirect
from django.contrib import auth
from django.urls import reverse
from django.contrib.auth.models import User
from MyWebSite.settings import LIMIT_TIME

from .utils import limit_ip
from .forms import LoginForm,RegisterForm

# Create your views here.
def login_limit_ip(request):
    if request.META.get('HTTP_X_FORWARDED_FOR'):
        ip = request.META.get("HTTP_X_FORWARDED_FOR")
    else:
        ip = request.META.get("REMOTE_ADDR")

    not_limit = True
    context = {}
    if limit_ip(request):
        not_limit = False  # 受限了不再进行post登录
        context['limit_msg'] = '对不起，您的访问过于频繁，请等待%d秒后再操作！'% LIMIT_TIME
    if not_limit and request.method == 'POST':
        # 请求方法是POST类型，说明是登录请求
        print(request.POST)
        login_form = LoginForm(request.POST)  # 将request中的参数传入到Form 类中
        if login_form.is_valid():
            # 判断数据有效
            user = login_form.cleaned_data['user']
            auth.login(request,user)
            return redirect(request.GET.get('referer'),reverse('index'))
    else:
        # 其他的方法，我们就刷新登录页面
        login_form = LoginForm()


    context['form']=login_form
    return render(request, 'login_limit_ip.html', context)



def login(request):
    if request.method == 'POST':
        # 请求方法是POST类型，说明是登录请求
        print(request.POST)
        login_form = LoginForm(request.POST)  # 将request中的参数传入到Form 类中
        if login_form.is_valid():
            # 判断数据有效
            user = login_form.cleaned_data['user']
            auth.login(request,user)
            return redirect(request.GET.get('referer'),reverse('index'))
    else:
        # 其他的方法，我们就刷新登录页面
        login_form = LoginForm()

    context = {}
    context['form']=login_form
    return render(request, 'login.html', context)

def logout(request):
    # 退出登录
    auth.logout(request)
    referer = request.META.get('HTTP_REFERER','login')
    return redirect(referer)

def register(request):
    if request.method == 'POST':
        # 请求方法是POST类型，说明是登录请求
        register_form = RegisterForm(request.POST)  # 将request中的参数传入到Form 类中
        if register_form.is_valid():
            username = register_form.cleaned_data['username']
            email = register_form.cleaned_data['email']
            password = register_form.cleaned_data['password']
            # 进行注册，实际上就是给User添加一条数据
            user = User.objects.create_user(username,email,password)
            user.save()

            # 注册成功后，直接登录并跳转到之前的页面
            user = auth.authenticate(username= username, password=password)
            auth.login(request,user)
            return redirect(request.GET.get('referer'), reverse('index'))

    else:
        # 其他的方法，我们就刷新登录页面
        register_form = RegisterForm()

    context = {}
    context['form']=register_form
    return render(request, 'register.html', context)

def user_center(request):
    context = {}
    return render(request, 'user_center.html', context)