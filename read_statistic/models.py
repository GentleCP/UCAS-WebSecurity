# django 库
from django.db import models
from django.db.models.fields import exceptions  # 包含了model中会抛出的异常
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone

# Create your models here.
class ReadNum(models.Model):
    '''
    阅读数量model，用于对不同app的文章资料阅读计数
    '''
    read_num = models.IntegerField(default=0)

    content_type = models.ForeignKey(ContentType,on_delete=models.DO_NOTHING) # 将ContentType绑定作为外键生成contenttype对象
    object_id = models.PositiveIntegerField() # 对象的id，确定了对象后根据id唯一定位对象
    content_object = GenericForeignKey('content_type','object_id') # 将上面两个合并成一个content对象

    def add_read_num(self):
        self.read_num += 1 # 添加一次阅读数量
        self.save()

class ReadNumExtendMethod():
    '''
    ReadNum 拓展方法类
    '''
    def get_read_num(self):
        '''
        获取阅读数方法，这个由Blog继承了，Blog页面的阅读数blog.get_read_num来自这
        :return: read_num字段值
        '''
        try:
            blog_ct = ContentType.objects.get_for_model(self)  # 获取到Blog对应的conttype对象
            # 通过blog的contenttype和blog的id找到对应的阅读对象
            readnum = ReadNum.objects.get(content_type=blog_ct, object_id=self.id)
            return readnum.read_num # 返回readnum对象的read_num字段
        except exceptions.ObjectDoesNotExist as e:
           return 0 # 还没有阅读过，返回0

class ReadDetail(models.Model):
    '''
    阅读情况详细信息，包括按天记录阅读数
    '''
    read_date = models.DateField(default = timezone.now)
    read_num = models.IntegerField(default=0)

    content_type = models.ForeignKey(ContentType, on_delete=models.DO_NOTHING)  # 将ContentType绑定作为外键生成contenttype对象
    object_id = models.PositiveIntegerField()  # 对象的id，确定了对象后根据id唯一定位对象
    content_object = GenericForeignKey('content_type', 'object_id')  # 将上面两个合并成一个content对象

    def add_read_num(self):
        self.read_num += 1  # 添加一次阅读数量
        self.save()
