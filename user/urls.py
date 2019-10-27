from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    # localhost:8000/user
    path('login/', views.login, name="login"),
    path('login_limit_ip/',views.login_limit_ip,name="login_limit_ip"),
    path('login_limit_captcha/', views.login_limit_captcha, name="login_limit_captcha"),
    path('user_center', views.user_center, name="user_center"),
    path('logout/', views.logout, name="logout"),
    path('register/', views.register, name="register"),
    path('login_slide_captcha/slide_captcha/', views.slide_captcha, name="slide_captcha"),
    path('login_slide_captcha/', views.login_slide_captcha, name="login_slide_captcha"),
    path('login-block-account/', views.login_block_account, name="login_block_account"),

]
