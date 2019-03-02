from django import forms
from django.db.models import ObjectDoesNotExist
from django.contrib.contenttypes.models import ContentType
from ckeditor.widgets import CKEditorWidget


class CommentForm(forms.Form):
    content_type = forms.CharField(widget=forms.HiddenInput())
    object_id = forms.IntegerField(widget=forms.HiddenInput())
    content = forms.CharField(widget=CKEditorWidget(config_name='comment_ckeditor'), label=False,
                              error_messages={'required': '你还没有输入评论哦'})

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
