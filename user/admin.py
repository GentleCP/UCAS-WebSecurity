from django.contrib import admin
from .models import HostInfo
from .models import LoginError
# Register your models here.

@admin.register(HostInfo)
class HostInfoAdmin(admin.ModelAdmin):
    list_display = ('id','host','count','start_time','is_lock')


@admin.register(LoginError)
class LoginErrorAdmin(admin.ModelAdmin):
    list_display = ('user','first_err_time', 'err_login_times', 'block_state')


