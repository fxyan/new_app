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
        comment.save()

        # 返回数据ajax
        data['status'] = 'SUCCESS'
        data['username'] = comment.user.username
        data['comment_time'] = comment.create_time
        data['text'] = comment.text
        # return redirect(referer)
    else:
        print('value', list(comment_form.errors.values())[0][0])
        # return render(request, 'error.html', {'message': comment_form.errors, 'redirect_to': referer})
        data['status'] = 'ERROR'
        data['message'] = list(comment_form.errors.values())[0]
    return JsonResponse(data)
