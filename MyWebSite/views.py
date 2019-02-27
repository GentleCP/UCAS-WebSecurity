from django.shortcuts import render,redirect
from django.contrib import auth
from django.urls import reverse
from django.contrib.auth.models import User

from .forms import LoginForm,RegisterForm

def get_index(request):
    context = {}
    return render(request,'index.html',context)

def login(request):
    if request.method == 'POST':
        # 请求方法是POST类型，说明是登录请求
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
    return render(request,'login.html',context)

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
    return render(request,'register.html',context)
