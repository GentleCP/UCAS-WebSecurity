from django.shortcuts import render,redirect
from django.contrib import auth
from django.urls import reverse
from django.contrib.auth.models import User

from MyWebSite.settings import LIMIT_TIME

from .utils import limit_ip
from .forms import LoginForm,RegisterForm,LoginForm_limit_captcha
from user import models
import time
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse

from user import create_captcha

from user.utils import check_account_state

# Create your views here.
def login_limit_ip(request):
    if request.META.get('HTTP_X_FORWARDED_FOR'):
        ip = request.META.get("HTTP_X_FORWARDED_FOR")
    else:
        ip = request.META.get("REMOTE_ADDR")

    not_limit = True
    context = {}
    if request.method =="POST" and limit_ip(request):
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
            context['err_msg'] = "用户名或密码错误！"
    else:
        # 其他的方法，我们就刷新登录页面
        login_form = LoginForm()


    context['form']=login_form
    return render(request, 'login_limit_ip.html', context)

title = ''

def login_limit_captcha(request):
    global title   #定义全局变量保存生成的验证码标签
    context = {}
    #title = title
    if request.method == 'POST':
        # 请求方法是POST类型，说明是登录请求
        print(request.POST)
        login_form = LoginForm_limit_captcha(request.POST)  # 将request中的参数传入到Form 类中
        if login_form.is_valid():
            #print('is valid')
            # 判断数据有效
            user = login_form.cleaned_data['user']
            captcha = login_form.cleaned_data['captcha']
            if title == captcha:
                #如果验证码认证成功则完成登陆，返回上一个页面
                auth.login(request,user)
                print(request.GET.get('referer'),reverse('index'))
                #if request.GET.get('referer') != None:
                return redirect(request.GET.get('referer'),reverse('index')) #返回上一个页面
            else:
                #如果验证码认证失败则刷新页面，刷新验证码
                img,title = create_captcha.create_captcha_set()
                context['err_msg'] = '验证码错误，请重新输入'

        else: 
            #如果认证失败则刷新页面面，刷新验证码 
            img,title = create_captcha.create_captcha_set()
            context['err_msg'] = '用户名或密码错误！'

    else:
        # 其他的方法，我们就刷新登录页面，刷新验证码
        img,title = create_captcha.create_captcha_set()
        login_form = LoginForm_limit_captcha()

    context['form']=login_form
    return render(request, 'login_limit_captcha.html', context)

@csrf_exempt
def slide_captcha(request):
    if request.method == "POST":
            username = request.POST.get('un')
            res = request.POST.get('result')
            t = str(time.time())
            if res == 'true':
                models.LoginCaptcha.objects.create(username=username, key= t)
                # captcha.append({username:time.time()})
                # print(captcha)

            dict = {'key': t,'username':username}
            return JsonResponse(dict)

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
    context = {}
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
            context['err_msg'] = "用户名或密码错误！"
    else:
        # 其他的方法，我们就刷新登录页面
        login_form = LoginForm()

    context['form']=login_form
    return render(request, 'login.html', context)


def login_block_account(request):
    """
    限制10min内登陆失败次数超过3次的账户
    :param request:
    :return:
    """
    context = dict()

    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        account_state = check_account_state(request)  # 当前账户的状态
        if account_state == 1:
            if login_form.is_valid():
                user = login_form.cleaned_data['user']
                auth.login(request, user)
                return redirect(request.GET.get('referer'), reverse('index'))

            else:
                context['limit_msg'] = '用户名或密码错误！'
        elif account_state == 0:  # 被封禁
            context['limit_msg'] = '您输错次数太多，请等待60s后再试！'
        elif account_state == -1:
            context['limit_msg'] = '用户名或密码错误！'
    else:
        login_form = LoginForm()

    context['form'] = login_form
    return render(request, 'login_block_account.html', context)


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


