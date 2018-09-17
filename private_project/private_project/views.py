from django.shortcuts import render
from django.contrib.contenttypes.models import ContentType
from blog.models import Blog
from .utils import get_seven_days_read_data, get_today_hot_read, get_yesterday_hot_read, get_week_hot_read


def home(request):
    context = {}
    blog_content_type = ContentType.objects.get_for_model(Blog)
    dates, seven_days_read_num = get_seven_days_read_data(blog_content_type)
    today_hot_read = get_today_hot_read(blog_content_type)
    yesterday_hot_read = get_yesterday_hot_read(blog_content_type)
    week_hot_read = get_week_hot_read()
    context['week_hot_read'] = week_hot_read
    context['yesterday_hot_read'] = yesterday_hot_read
    context['today_hot_read'] = today_hot_read
    context['read_num'] = seven_days_read_num
    context['dates'] = dates
    return render(request, 'home.html', context)
