from django import template
from django.contrib.contenttypes.models import ContentType

from ..models import Comment
from ..forms import CommentForm
register = template.Library()  # 获取注册器

@register.simple_tag  # simple_tag允许传入多个参数
def get_comment_num(obj):
    content_type = ContentType.objects.get_for_model(obj)  # 通过对象获取content_type
    comment_num = Comment.objects.filter(content_type=content_type, object_id=obj.id).count()  # 评论数
    return comment_num

@register.simple_tag
def get_comment_form(obj):
    content_type = ContentType.objects.get_for_model(obj)  # 通过对象获取content_type
    comment_form = CommentForm(initial={
        'content_type': content_type.model,
        'object_id': obj.id,
        'reply_id': 0})
    return comment_form

@register.simple_tag
def get_comments(obj):
    content_type = ContentType.objects.get_for_model(obj)  # 通过对象获取content_type
    comments = Comment.objects.filter(content_type=content_type,
                           object_id=obj.id,
                           parent=None)  # parent=None说明是原始评论
    return comments.order_by('-created_time')