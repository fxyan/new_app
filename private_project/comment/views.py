from django.shortcuts import render, redirect, reverse
from django.http import JsonResponse
from .models import Comment
from django.contrib.contenttypes.models import ContentType
from private_project.forms import CommentForm


def comment(request):
    # 一个重定向的地址，如果没有就返回主页
    referer = request.META.get('HTTP_REFERER', reverse('home'))
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
        data['comment_time'] = comment.create_time.strftime("%Y-%m-%d %H:%M:%S")
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
