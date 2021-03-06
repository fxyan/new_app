from django.shortcuts import reverse
from django.http import JsonResponse
from .models import Comment
from private_project.forms import CommentForm


def comment(request):
    # 向表单中传入user值方便进行验证
    comment_form = CommentForm(request.POST, user=request.user)
    data = {}
    # 保存数据
    if comment_form.is_valid():
        comment = Comment()
        comment.user = comment_form.cleaned_data['user']
        comment.text = comment_form.cleaned_data['comment']
        comment.content_object = comment_form.cleaned_data['content_type']
        parent = comment_form.cleaned_data['reply_comment_id']
        if parent is not None:
            comment.root = parent.root if parent.root is not None else parent
            comment.parent = parent
            comment.reply = parent.user
        comment.save()

        # 返回数据ajax
        data['status'] = 'SUCCESS'
        data['username'] = comment.user.username
        data['comment_time'] = comment.create_time.timestamp()
        data['text'] = comment.text
        if parent is not None:
            data['reply_user'] = comment.reply.username
        else:
            data['reply_user'] = ''
        data['comment_pk'] = comment.pk
        data['root_pk'] = comment.root.pk if comment.root is not None else ''
    else:
        data['status'] = 'ERROR'
        # 错误信息
        data['message'] = list(comment_form.errors.values())[0]
    return JsonResponse(data)
