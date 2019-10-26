from django.db import models


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



