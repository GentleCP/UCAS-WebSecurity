import time

from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render,redirect
from django.contrib import auth
from django.urls import reverse
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt

from user import models
from .forms import LoginForm,RegisterForm

@csrf_exempt
def slide_captcha(request):
    if request.method == "POST":
            username = request.POST.get('un')
            res = request.POST.get('result')
            t = str(time.time())
            print(username)
            print(res)
            if res == 'true':
                models.LoginCaptcha.objects.create(username=username, key= t)
                # captcha.append({username:time.time()})
                # print(captcha)

            dict = {'key': t,'username':username}
            return JsonResponse(dict)


# Create your views here.
@csrf_exempt
def login_slide_captcha(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        if models.LoginCaptcha.objects.filter(username=username).count() != 1 :
            return HttpResponse('fail')
        else:
            user = models.LoginCaptcha.objects.get(username=username)
            print(user)
            if user:
                if (user.key == request.POST.get('key')):
                    models.LoginCaptcha.objects.get(username=request.POST.get('username')).delete()
                    # 请求方法是POST类型，说明是登录请求
                    login_form = LoginForm(request.POST)  # 将request中的参数传入到Form 类中
                    print(request.POST)
                    if login_form.is_valid():
                        # 判断数据有效
                        user = login_form.cleaned_data['user']
                        auth.login(request, user)
                        return HttpResponse('success')
                        # return redirect(request.GET.get('referer'),reverse('index'))
    else:
        # 其他的方法，我们就刷新登录页面
        login_form = LoginForm()

    context = {}
    context['form']=login_form
    return render(request, 'login_slide.html', context)

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