from django.db import models
from django.contrib.auth.models import User # 后台用户模块
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

# Create your models here.
class ReadHistory(models.Model):
    '''
    阅读历史，根据用户信息对应记录所有可以阅读的对象的阅读记录
    '''
    content_type = models.ForeignKey(ContentType,on_delete=models.DO_NOTHING)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type','object_id')

    user = models.ForeignKey(User,on_delete=models.DO_NOTHING,verbose_name="用户名")
    last_read_time = models.DateTimeField(verbose_name="上次阅读时间")