from django.contrib.contenttypes.models import ContentType
from django.db.models import Sum
from read_statistics.models import ReadNum, ReadNumDetail
from blog.models import Blog
from django.utils import timezone
import datetime


# 增加阅读数量 并且返回cookie
def get_readnum(request, obj):
    ct = ContentType.objects.get_for_model(obj)
    key = '{}_{}_read'.format(ct.model, obj.pk)
    if request.COOKIES.get(key) is None:
        # 每篇文章的阅读数据+1
        readnum, create = ReadNum.objects.get_or_create(content_type=ct, object_id=obj.pk)
        readnum.read_num += 1
        readnum.save()
        # 按照时间的阅读数据+1
        date = timezone.now().date()
        readnum_detail, create = ReadNumDetail.objects.get_or_create(content_type=ct, object_id=obj.pk, date=date)
        readnum_detail.read_num += 1
        readnum_detail.save()
    return key


def get_seven_days_read_data(content_type):
    time = []
    dates = []
    today = timezone.now().date()
    for i in range(7, 0, -1):
        date = today - datetime.timedelta(days=i)
        dates.append(date.strftime('%m/%d'))
        read_num_detail = ReadNumDetail.objects.filter(content_type=content_type, date=date)
        result = read_num_detail.aggregate(read_num_sum=Sum('read_num'))
        time.append(result['read_num_sum'] or 0)
    return dates, time


def get_today_hot_read(content_type):
    today = timezone.now().date()
    today_hot_read = ReadNumDetail.objects.filter(
        content_type=content_type,
        date=today
    ).order_by('-read_num')[:7]
    return today_hot_read


def get_yesterday_hot_read(content_type):
    today = timezone.now().date()
    date = today - datetime.timedelta(days=1)
    yesterday_hot_read = ReadNumDetail.objects.filter(
        content_type=content_type,
        date=date
    ).order_by('-read_num')[:7]
    return yesterday_hot_read


def get_week_hot_read():
    today = timezone.now().date()
    date = today - datetime.timedelta(days=7)
    week_hot_read = Blog.objects.filter(
        read_num__date__lt=today,
        read_num__date__gte=date
        #  这里进行了修改read_num
    ).values('id', 'title').annotate(read_num_sum=Sum('read_num__read_num')).order_by('-read_num_sum')[:7]
    return week_hot_read
