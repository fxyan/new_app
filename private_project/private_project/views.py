from django.shortcuts import render, redirect, reverse
from read_statistics.models import ReadNumDetail
from django.contrib.contenttypes.models import ContentType
from django.contrib import auth
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db.models import Sum
from django.utils import timezone
from blog.models import Blog
import datetime
from .utils import get_seven_days_read_data, get_today_hot_read, get_yesterday_hot_read, get_week_hot_read
from.forms import LoginForm, RegisterForm


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


def login(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            print('clean_date', login_form.cleaned_data)
            user = login_form.cleaned_data['user']
            auth.login(request, user)
            return redirect(request.GET.get('form', reverse('home')))
    else:
        login_form = LoginForm()
    context = {}
    context['login_form'] = login_form
    return render(request, 'login.html', context)


def register(request):
    if request.method == 'POST':
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            username = register_form.cleaned_data['username']
            password = register_form.cleaned_data['password']
            email = register_form.cleaned_data['email']
            user = User.objects.create_user(username, email, password)
            user.save()

            user = authenticate(username=username, password=password)
            auth.login(request, user)
            print('重定向')
            return redirect(request.GET.get('form', reverse('home')))
    else:
        register_form = RegisterForm()
    context = {}
    context['register_form'] = register_form
    return render(request, 'register.html', context)
