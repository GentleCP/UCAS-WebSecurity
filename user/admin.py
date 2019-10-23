from django.contrib import admin
from .models import HostInfo
# Register your models here.

@admin.register(HostInfo)
class HostInfoAdmin(admin.ModelAdmin):
    list_display = ('id','host','count','start_time','is_lock')