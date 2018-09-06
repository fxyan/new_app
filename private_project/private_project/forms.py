from django import forms
from django.contrib import auth
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    username = forms.CharField(
        label='用户名',
        max_length=20,
        widget=forms.TextInput(attrs={'placeholder': '请输入用户名', 'class': 'form-control'})
    )
    password = forms.CharField(
        label='密码',
        min_length=5,
        widget=forms.PasswordInput(attrs={'placeholder': '请输入密码', 'class': 'form-control'})
    )

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        user = auth.authenticate(username=username, password=password)
        if user is None:
            raise forms.ValidationError('用户名密码不正确233333')
        else:
            self.cleaned_data['user'] = user
        return self.cleaned_data


class RegisterForm(forms.Form):
    username = forms.CharField(
        label='用户名',
        max_length=20,
        min_length=3,
        widget=forms.TextInput(attrs={'placeholder': '请输入3-20位用户名', 'class': 'form-control'})
    )
    email = forms.EmailField(
        label='邮箱',
        required=False,
        widget=forms.EmailInput(attrs={'placeholder': '请输入邮箱', 'class': 'form-control'})
    )
    password = forms.CharField(
        label='密码',
        min_length=5,
        widget=forms.PasswordInput(attrs={'placeholder': '请输入大于5位的密码', 'class': 'form-control'})
    )
    password_again = forms.CharField(
        label='重复密码',
        min_length=5,
        widget=forms.PasswordInput(attrs={'placeholder': '请重复密码', 'class': 'form-control'})
    )

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('邮箱已存在')
        return email

    def clean_username(self):
        print(111111111)
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('用户名已存在')
        return username

    def clean_password_again(self):
        password = self.cleaned_data['password']
        password_again = self.cleaned_data['password_again']
        if password_again != password:
            print(11111112)
            raise forms.ValidationError('两次输入的密码不相同')
        return password_again


class CommentForm(forms.Form):
    object_id = forms.IntegerField(widget=forms.HiddenInput)
    content_type = forms.CharField(widget=forms.HiddenInput)
    comment = forms.CharField(
        label='评论',
        max_length=20,
        widget=forms.Textarea(attrs={'placeholder': '请输入评论'})
    )
