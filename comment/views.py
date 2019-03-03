from django.shortcuts import render,redirect
from django.contrib.contenttypes.models import ContentType
from django.http import JsonResponse
from django.urls import reverse

from .models import Comment
from .forms import CommentForm

# Create your views here.

def submit_comment(request):
    '''
    提交评论方法，该评论方法应对所有拥有评论的model提供
    :param request:
    :return:
    '''
    referer = request.META.get('HTTP_REFERER', reverse('index'))
    user = request.user
    comment_form = CommentForm(request.POST)  #request.POST 是一个字典
    data = {}
    if comment_form.is_valid() and user.is_authenticated:
        # 提交了一个有效评论
        comment = Comment(content = comment_form.cleaned_data['content'],
                          content_object = comment_form.cleaned_data['content_object'],
                          user=user)
        parent = comment_form.cleaned_data['parent']
        if parent is not None:
            # parent这一属性不为None，说明是回复
            comment.parent = parent
            comment.root = parent.root if parent.root is not None else parent
            comment.to_user = parent.user
            data['to_user'] = parent.user.username # 在前台显示对xxx的回复
        else:
            data['to_user'] = ''  # 这是条一级评论
        comment.save()
        # return redirect(referer)
        data['status'] = 'SUCCESS'
        data['id'] = comment.id  # 记录评论的id
        data['root_id'] = comment.root.id if comment.root.id is not None else ''
        data['username'] = comment.user.username
        data['created_time'] = comment.created_time.strftime("%Y-%m-%d %H:%M:%S")
        data['content'] = comment.content
    else:
        # 提交无效评论，如评论内容为空
        data['status'] = 'FAIL'
        data['error_message'] = list(comment_form.errors.values())[0]

    return JsonResponse(data)
