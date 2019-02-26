from django.shortcuts import render,redirect
from django.contrib import auth
from django.urls import reverse
def get_index(request):
    context = {}
    return render(request,'index.html',context)

def login(request):
    context = {}
    return render(request,'login.html',context)

def logout(request):
    # 退出登录
    auth.logout(request)
    referer = request.META.get('HTTP_REFERER','login')
    return redirect(referer)

def login_check(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(request, username=username, password=password)
    # referer = request.META.get('HTTP_REFERER',reverse('index'))
    if user is not None:
        auth.login(request, user)
        # Redirect to a success page.
        return redirect(reverse('index')) # 登录成功重定向到进行登录的页
    else:
        # Return an 'invalid login' error message.
        context = {}
        context['error_message'] = '用户名或密码不正确，登录失败！'
        return render(request,'login.html',context) # 登录失败返回login.html 并提示错误信息