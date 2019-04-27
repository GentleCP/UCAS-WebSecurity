from django import forms
from django.db.models import ObjectDoesNotExist
from django.contrib.contenttypes.models import ContentType
from ckeditor.widgets import CKEditorWidget
from .models import Comment

class CommentForm(forms.Form):
    content_type = forms.CharField(widget=forms.HiddenInput())
    object_id = forms.IntegerField(widget=forms.HiddenInput())
    content = forms.CharField(widget=CKEditorWidget(config_name='comment_ckeditor'), label=False,
                              error_messages={'required': '你还没有输入评论哦'})
    reply_id = forms.IntegerField(widget=forms.HiddenInput(attrs={'id':'id_reply'}))

    def clean(self):
        # 验证评论的对象是否存在
        content_type = self.cleaned_data['content_type']
        object_id = self.cleaned_data['object_id']
        try:
            model = ContentType.objects.get(model=content_type).model_class()  # 获取content_type对应的类
            model_obj = model.objects.get(id=object_id)
            self.cleaned_data['content_object'] = model_obj

        except ObjectDoesNotExist:
            raise forms.ValidationError('评论对象不存在哦')

        return self.cleaned_data

    def clean_reply_id(self):
        # 对reply_id进行验证
        reply_id = self.cleaned_data['reply_id']
        if reply_id < 0:
            raise forms.ValidationError('哦豁，好像出现错误了哦')
        elif reply_id ==  0:
            # 是0说明是一般评论，不是回复
            self.cleaned_data['parent'] = None
        else:
            if Comment.objects.filter(id = reply_id).exists():
                # 如果reply_id对应的评论或回复存在
                self.cleaned_data['parent'] = Comment.objects.get(id=reply_id)
            else:
                # 该条评论或回复可能被删除了
                raise forms.ValidationError('该评论找不到了哦，试试刷新页面')
        return reply_id