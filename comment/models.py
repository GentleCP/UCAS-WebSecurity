from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User # 后台用户模块

# Create your models here.
class Comment(models.Model):
    '''
    评论model，针对博客进行评论
    '''
    # 因为评论要针对博客，因此需要博客id作为外键，将其与ContentType联合绑定成一个外键
    content_type = models.ForeignKey(ContentType, on_delete=models.DO_NOTHING)  # 将ContentType绑定作为外键生成contenttype对象
    object_id = models.PositiveIntegerField()  # 对象的id，确定了对象后根据id唯一定位对象
    content_object = GenericForeignKey('content_type', 'object_id')  # 将上面两个合并成一个content对象

    content = models.TextField(verbose_name='评论内容')
    user = models.ForeignKey(User,on_delete=models.DO_NOTHING, verbose_name='评论用户') # 评论用户
    created_time = models.DateTimeField(auto_now_add=True,verbose_name='评论时间')
    class Meta:
        ordering = ['-created_time', ]  # 这里让前端网页在对从request获取到的数据排序按照创建时间由新到旧