from django import template
from django.contrib.contenttypes.models import ContentType
from ..models import Comment
from private_project.forms import CommentForm

register = template.Library()


@register.simple_tag
def get_comment_num(obj):
    content_type = ContentType.objects.get_for_model(obj)
    comment = Comment.objects.filter(
        content_type=content_type,
        object_id=obj.pk
    ).count()
    return comment


@register.simple_tag
def get_comment_forms(obj):
    content_type = ContentType.objects.get_for_model(obj)
    comment_forms = CommentForm(initial={
        'content_type': content_type,
        'object_id': obj.pk,
        'reply_comment_id': 0
    })
    return comment_forms


@register.simple_tag
def get_comment(obj):
    content_type = ContentType.objects.get_for_model(obj)
    comment = Comment.objects.filter(
        content_type=content_type,
        object_id=obj.id,
        parent=None
    ).order_by('-create_time')
    return comment
