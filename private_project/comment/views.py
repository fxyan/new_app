from django.shortcuts import reverse
from django.http import JsonResponse
from .models import Comment
from private_project.forms import CommentForm


def comment(request):
    comment_form = CommentForm(request.POST, user=request.user)
    data = {}
    if comment_form.is_valid():
        comment = Comment()
        comment.user = comment_form.cleaned_data['user']
        comment.text = comment_form.cleaned_data['comment']
        comment.content_object = comment_form.cleaned_data['content_type']
        parent = comment_form.cleaned_data['reply_comment_id']
        print(parent)
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
        print('value', list(comment_form.errors.values())[0][0])
        data['status'] = 'ERROR'
        data['message'] = list(comment_form.errors.values())[0]
    return JsonResponse(data)
