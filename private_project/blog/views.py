from django.db.models import Count
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Blog, BlogType
from private_project.utils import get_readnum


# 分页函数
def get_paginator_list(request, blog_list):
    context = {}
    # 每页分5个
    blog_page = Paginator(blog_list, 5)
    page = request.GET.get('page', 1)
    # 处理页码 页码不合法也可以处理
    page_of_blogs = blog_page.get_page(page)
    currentr_page_num = page_of_blogs.number
    # 返回合适的页码列表
    pages_num = list(
        range(max(1, currentr_page_num - 2), currentr_page_num)
    ) + list(
        range(currentr_page_num, min(currentr_page_num + 2, blog_page.num_pages) + 1)
    )
    # 添加省略号
    if pages_num[0] > 2:
        pages_num.insert(0, '...')
    if pages_num[-1] < blog_page.num_pages - 1:
        pages_num.append('...')
    # 添加首页和尾页
    if pages_num[0] != 1:
        pages_num.insert(0, 1)
    if pages_num[-1] != blog_page.num_pages:
        pages_num.append(blog_page.num_pages)

    # 日期归档计数
    blog_dates = Blog.objects.dates('create_time', 'month', order='DESC')
    blogs_count = {}
    for blog_date in blog_dates:
        blog_count = Blog.objects.filter(
            create_time__year=blog_date.year,
            create_time__month=blog_date.month
        ).count()
        blogs_count[blog_date] = blog_count

    context['pages_num'] = pages_num
    context['page_of_blogs'] = page_of_blogs
    context['blog_dates'] = blogs_count
    context['blog_types'] = BlogType.objects.annotate(blog_count=Count('blog'))
    return context


def blog_list(request):
    blogs = Blog.objects.all()
    context = get_paginator_list(request, blogs)
    return render(request, 'blog_list.html', context)


def blog_detail(request, blog_pk):
    context = {}
    # 无效页面返回404
    blog = get_object_or_404(Blog, pk=blog_pk)
    # 返回cookie值
    read_key = get_readnum(request, blog)
    context['blog'] = blog
    context['previous_blog'] = Blog.objects.filter(create_time__lt=blog.create_time).first()
    context['next_blog'] = Blog.objects.filter(create_time__gt=blog.create_time).last()
    response = render(request, 'blog_detail.html', context)
    # 方便计数我们设置cookie值
    response.set_cookie(read_key, 'true')
    return response


def blog_with_type(request, blog_type_pk):
    # 无效类型返回404
    blog_type = get_object_or_404(BlogType, pk=blog_type_pk)
    blogs = Blog.objects.filter(blog_type=blog_type)
    context = get_paginator_list(request, blogs)
    context['blog_type'] = blog_type
    return render(request, 'blog_with_type.html', context)


# 返回每个月的不同博客
def blog_with_date(request, year, month):
    blogs = Blog.objects.filter(create_time__year=year, create_time__month=month)
    context = get_paginator_list(request, blogs)
    context['blogs'] = blogs
    context['blog_with_date'] = '{}年{}月'.format(year, month)
    return render(request, 'blog_with_date.html', context)

