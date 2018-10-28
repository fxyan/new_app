from django import forms
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.db.models import ObjectDoesNotExist
from ckeditor.widgets import CKEditorWidget
from comment.models import Comment


class CommentForm(forms.Form):
    # 在tags里面进行了修改
    object_id = forms.IntegerField(widget=forms.HiddenInput)
    content_type = forms.CharField(widget=forms.HiddenInput)
    comment = forms.CharField(
        label='评论',
        # 更改小部件使用富文本编辑器
        widget=CKEditorWidget(config_name='comment_ckeditor'),
        error_messages={'required': '评论不能为空'}
    )
    reply_comment_id = forms.IntegerField(widget=forms.HiddenInput(attrs={'id': 'reply_comment_id'}))

    # 这里调用的父类的方法将user传了进来方便进行验证
    def __init__(self, *args, **kwargs):
        if 'user' in kwargs:
            self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

    def clean(self):
        # 判断用户是否登录
        if self.user.is_authenticated:
            self.cleaned_data['user'] = self.user
        else:
            raise forms.ValidationError('用户尚未登录')
        object_id = self.cleaned_data['object_id']
        content_type = self.cleaned_data['content_type']
        try:
            # 返回类模型
            model_class = ContentType.objects.get(model=content_type).model_class()
            model_obj = model_class.objects.get(pk=object_id)
            self.cleaned_data['content_type'] = model_obj
        except ObjectDoesNotExist:
            raise forms.ValidationError('评论对象不存在')
        return self.cleaned_data

    # 验证回复对象的id 来检测父评论
    def clean_reply_comment_id(self):
        reply_comment_id = self.cleaned_data['reply_comment_id']
        if reply_comment_id < 0:
            raise forms.ValidationError('回复出错')
        elif reply_comment_id == 0:
            self.cleaned_data['parent'] = None
        elif Comment.objects.filter(pk=reply_comment_id).exists():
            self.cleaned_data['parent'] = Comment.objects.get(pk=reply_comment_id)
        else:
            raise forms.ValidationError('回复出错')
        return self.cleaned_data['parent']
