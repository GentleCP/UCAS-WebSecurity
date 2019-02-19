# django 的库
from django.contrib import admin

# 本地库
from .models import Blog,BlogType
# Register your models here.

@admin.register(BlogType)
class BlogTypeAdmin(admin.ModelAdmin):
    list_display = ('type_name',)

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('id','title','blog_type','get_read_num')
    ordering = ['id',]