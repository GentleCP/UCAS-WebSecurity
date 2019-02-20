# django 的库
from django.db import models
from django.contrib.auth.models import User

# 第三方库
from ckeditor_uploader.fields import RichTextUploadingField
from mdeditor.fields import MDTextField

# 本地库
from read_statistic.models import ReadNumExtendMethod


# Create your models here.
class BlogType(models.Model):
    type_name = models.CharField(max_length=30, verbose_name="博客类型")

    def __str__(self):
        return self.type_name


class Blog(models.Model, ReadNumExtendMethod):
    title = models.CharField(max_length=40, verbose_name="标题")
    blog_type = models.ForeignKey(BlogType, on_delete=models.DO_NOTHING, verbose_name="博客类型")
    # 这里的User类是django自带的，导入superuser作为用户名，需要import django.contrib.auth.models
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING, verbose_name="作者")
    content = RichTextUploadingField(verbose_name="内容")
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    last_modified_time = models.DateTimeField(auto_now=True, verbose_name="上次修改时间")

    def __str__(self):
        return "[Title:%s]" % self.title

    class Meta:
        ordering = ['-created_time', ]  # 这里让前端网页在对从request获取到的数据排序按照创建时间由新到旧
