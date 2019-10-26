# django 库
from django.contrib import admin

# 本地库
from .models import ReadNum
from .models import ReadDetail

# Register your models here.
@admin.register(ReadNum)
class ReadNumAdmin(admin.ModelAdmin):
    list_display = ['id','content_type','object_id', 'read_num']

@admin.register(ReadDetail)
class ReadDetailAdmin(admin.ModelAdmin):
    list_display = ['id','content_type','object_id', 'read_num','read_date']