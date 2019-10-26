from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    # localhost:8000/user
    path('login/', views.login, name="login"),
    path('user_center/', views.user_center, name="user_center"),
    path('logout/', views.logout, name="logout"),
    path('register/', views.register, name="register"),
    path('login_slide_captcha/slide_captcha/', views.slide_captcha, name="slide_captcha"),
    path('login_slide_captcha/', views.login_slide_captcha, name="login_slide_captcha"),
]
