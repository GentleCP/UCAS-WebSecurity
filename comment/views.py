from django.shortcuts import render,redirect
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse

from .models import Comment
# Create your views here.

def submit_comment(request):
    '''
    提交评论方法，该评论方法应对所有拥有评论的model提供
    :param request:
    :return:
    '''
    referer = request.META.get('HTTP_REFERER', reverse('index'))

    user = request.user
    content = request.POST.get('content','')

    #通过model名称一步步获取到model object，即Comment model中的content_type字段
    model_str = request.POST.get('model', '')
    model = ContentType.objects.get(model = model_str).model_class()
    obj_id = request.POST.get('object_id','')
    model_obj = model.objects.get(id = obj_id)

    # 每次评论都是一个新评论，需创建一个Comment对象,如果评论内容不为空才创建
    if content != '':
        comment = Comment(content=content,user=user,content_object = model_obj)
        comment.save()
    return redirect(referer) # 提交一个评论后重定向到当前页面 == 刷新
