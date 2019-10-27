from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class HostInfo(models.Model):
    """
    访问的主机信息
    """
    host = models.CharField(max_length=32)  # 主机ip
    count = models.IntegerField()  # 访问次数
    start_time = models.DateTimeField()  # 第一次访问时间
    is_lock = models.IntegerField(default=0)  # 是否限制,0：不限，1：受限


class LoginCaptcha(models.Model):
    """
        slide key table
    """
    username = models.CharField(max_length=32)
    key = models.CharField(max_length=32)


class LoginError(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, default=0)
    first_err_time = models.FloatField()  # 第一次输错密码的时间，距离1970年的秒数
    err_login_times = models.IntegerField()  # 该段时间内登陆失败的次数
    block_state = models.BooleanField(default=False)  # 账户是否在封禁状态，True表示封禁，False表示正常


