from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User  # 后台用户模块


# Create your models here.
class Comment(models.Model):
    '''
    评论model，既是对对象的评论也可以是对评论的评论
    '''
    # 因为评论要针对博客，因此需要博客id作为外键，将其与ContentType联合绑定成一个外键
    content_type = models.ForeignKey(ContentType, on_delete=models.DO_NOTHING)  # 将ContentType绑定作为外键生成contenttype对象
    object_id = models.PositiveIntegerField()  # 对象的id，确定了对象后根据id唯一定位对象
    content_object = GenericForeignKey('content_type', 'object_id')  # 将上面两个合并成一个content对象

    content = models.TextField(verbose_name='评论内容')
    user = models.ForeignKey(User, related_name="comments", on_delete=models.DO_NOTHING, verbose_name='评论用户')  # 评论用户
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='评论时间')

    root = models.ForeignKey('self',related_name="root_comment",null=True,on_delete=models.DO_NOTHING)  #该评论最初的根评论
    parent = models.ForeignKey('self', null=True, related_name="parent_comment", on_delete=models.DO_NOTHING,
                               verbose_name="父级评论")  # 评论的上级，指明该评论是针对哪个评论的评论
    to_user = models.ForeignKey(User, related_name="replies", null=True, on_delete=models.DO_NOTHING,
                                verbose_name="回复的用户")  # 该评论用户向谁回复了

    def __str__(self):
        # 显示评论对象
        return str(self.content_object) + '(' + str(self.object_id) + ')' + ':' + self.content

    class Meta:
        ordering = ['created_time', ]  # 这里让前端网页在对从request获取到的数据排序按照创建时间由新到旧
