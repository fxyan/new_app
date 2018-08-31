from django.shortcuts import render
from read_statistics.models import ReadNumDetail
from django.contrib.contenttypes.models import ContentType
from django.db.models import Sum
from django.utils import timezone
from blog.models import Blog
import datetime
from .utils import get_seven_days_read_data, get_today_hot_read, get_yesterday_hot_read, get_week_hot_read


def home(request):
    context = {}
    blog_content_type = ContentType.objects.get_for_model(Blog)
    dates, seven_days_read_num = get_seven_days_read_data(blog_content_type)
    today_hot_read = get_today_hot_read(blog_content_type)
    yesterday_hot_read = get_yesterday_hot_read(blog_content_type)
    week_hot_read = get_week_hot_read(blog_content_type)
    print(week_hot_read)
    context['week_hot_read'] = week_hot_read
    context['yesterday_hot_read'] = yesterday_hot_read
    context['today_hot_read'] = today_hot_read
    context['read_num'] = seven_days_read_num
    context['dates'] = dates
    return render(request, 'home.html', context)
