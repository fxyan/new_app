import random
import string
import time
from django.shortcuts import render, redirect, reverse
from django.http import JsonResponse
from django.contrib import auth
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.mail import send_mail
from.forms import LoginForm, RegisterForm, ChangeEmailForm, ChangePasswordForm, ForgetPasswordForm


def login(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = login_form.cleaned_data['user']
            auth.login(request, user)
            return redirect(request.GET.get('form', reverse('home')))
    else:
        login_form = LoginForm()
    context = {}
    context['login_form'] = login_form
    return render(request, 'user/login.html', context)


def register(request):
    if request.method == 'POST':
        register_form = RegisterForm(request.POST, request=request)
        if register_form.is_valid():
            username = register_form.cleaned_data['username']
            password = register_form.cleaned_data['password']
            email = register_form.cleaned_data['email']
            user = User.objects.create_user(username, email, password)
            user.save()

            # 清除session
            del request.session['register_code']

            user = authenticate(username=username, password=password)
            auth.login(request, user)
            return redirect(request.GET.get('form', reverse('home')))
    else:
        register_form = RegisterForm()
    context = {}
    context['register_form'] = register_form
    return render(request, 'user/register.html', context)


def logout(request):
    auth.logout(request)
    return redirect(reverse('home'))


def user_info(request):
    return render(request, 'user/user_info.html')


def change_password(request):
    redirect_to = reverse('home')
    if request.method == 'POST':
        change_password_form = ChangePasswordForm(request.POST, user=request.user)
        if change_password_form.is_valid():
            new_password = change_password_form.cleaned_data['password_again']
            user = request.user
            user.set_password(new_password)
            user.save()
            auth.logout(request)
            return redirect(redirect_to)
    else:
        change_password_form = ChangePasswordForm()
    context = {}
    context['field_title'] = '更改密码'
    context['redirect_to'] = redirect_to
    context['form'] = change_password_form
    return render(request, 'form.html', context)


def change_email(request):
    redirect_to = request.GET.get('form', reverse('home'))
    if request.method == 'POST':
        change_email_form = ChangeEmailForm(request.POST, request=request)
        if change_email_form.is_valid():
            email = change_email_form.cleaned_data['email']
            user = request.user
            user.email = email
            user.save()
            # 清除session
            del request.session['register_code']
            return redirect(redirect_to)
    else:
        change_email_form = ChangeEmailForm
    context = {}
    context['field_title'] = '绑定邮箱'
    context['redirect_to'] = redirect_to
    context['form'] = change_email_form
    return render(request, 'user/bind_email.html', context)


def forget_password(request):
    redirect_to = reverse('login')
    if request.method == 'POST':
        forget_password_form = ForgetPasswordForm(request.POST, request=request)
        if forget_password_form.is_valid():
            email = forget_password_form.cleaned_data['email']
            new_password = forget_password_form.cleaned_data['new_password']
            user = User.objects.get(email=email)
            user.set_password(new_password)
            user.save()
            # 清除session
            del request.session['forget_password_code']
            return redirect(redirect_to)
    else:
        forget_password_form = ForgetPasswordForm()
    context = {}
    context['field_title'] = '更改密码'
    context['redirect_to'] = redirect_to
    context['form'] = forget_password_form
    return render(request, 'user/forget_password.html', context)


def send_verification_code(request):
    data = {}
    email = request.GET.get('email', '')
    send_for = request.GET.get('send_for', '')
    if email != '':
        # 这里使用了python的一些标准库，random.sample返回指定序列中随机获取k个元素返回
        #  string.ascii_letters显示所有的字符 string.digits显示所有的数字
        code = ''.join(random.sample(string.ascii_letters + string.digits, 4))
        request.session['bind_email_code'] = code
        now = int(time.time())
        send_email_time = request.session.get('send_email_time', 0)
        if now - send_email_time < 30:
            data['status'] = 'ERROR'
        else:
            request.session[send_for] = code
            request.session['send_email_time'] = now
            send_mail(
                '绑定邮箱',
                '欢迎注册codelink分享你的见解。\n 验证码:{}'.format(code),
                '1350821504@qq.com',
                [email],
                fail_silently=False,
            )
            data['status'] = 'SUCCESS'
    return JsonResponse(data)
