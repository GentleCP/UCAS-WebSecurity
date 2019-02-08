from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class BlogType(models.Model):
    type_name = models.CharField(max_length=30,verbose_name="博客类型")

    def __str__(self):
        return self.type_name


class Blog(models.Model):
    title = models.CharField(max_length=40,verbose_name="标题")
    blog_type = models.ForeignKey(BlogType, on_delete=models.DO_NOTHING, verbose_name="博客类型")
    # 这里的User类是django自带的，导入superuser作为用户名，需要import django.contrib.auth.models
    author = models.ForeignKey(User,on_delete=models.DO_NOTHING,verbose_name="作者")
    content = models.TextField(verbose_name="内容")
    created_time = models.DateTimeField(auto_now_add=True,verbose_name="创建时间")
    last_modified_time = models.DateTimeField(auto_now=True,verbose_name="上次修改时间")

    def __str__(self):
        return "<Blog:%s>" % self.title

    class Meta:
        ordering = ['-created_time',]