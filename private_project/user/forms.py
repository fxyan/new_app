from django import forms
from django.contrib import auth
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    username_or_email = forms.CharField(
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
        username_or_email = self.cleaned_data['username_or_email']
        password = self.cleaned_data['password']
        user = auth.authenticate(username=username_or_email, password=password)
        if user is None:
            if User.objects.filter(email=username_or_email).exists():
                username = User.objects.get(email=username_or_email).username
                user = auth.authenticate(username=username, password=password)
                if user is not None:
                    self.cleaned_data['user'] = user
                    return self.cleaned_data
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
    verification_code = forms.CharField(
        label='输入验证码',
        required=False,
        widget=forms.TextInput(attrs={'placeholder': '点击"发送验证码"到你输入的邮箱', 'class': 'form-control'})
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

    def __init__(self, *args, **kwargs):
        if 'request' in kwargs:
            self.request = kwargs.pop('request')
        super().__init__(*args, **kwargs)

    def clean_verification_code(self):
        verification_code = self.cleaned_data.get('verification_code', '')
        if verification_code == '':
            raise forms.ValidationError('验证码不能为空')
        code = self.request.session.get('register_code', '')
        if not (code != '' and code == verification_code):
            raise forms.ValidationError('验证码错误')
        return self.cleaned_data

    def clean_email(self):
        email = self.cleaned_data['email']
        if email == '':
            raise forms.ValidationError('邮箱不能为空')
        elif User.objects.filter(email=email).exists():
            raise forms.ValidationError('邮箱已存在')
        return email

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('用户名已存在')
        return username

    def clean_password_again(self):
        password = self.cleaned_data['password']
        password_again = self.cleaned_data['password_again']
        if password_again != password:
            raise forms.ValidationError('两次输入的密码不相同')
        return password_again


class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(
        label='旧的密码',
        min_length=5,
        widget=forms.PasswordInput(attrs={'placeholder': '请输入原密码', 'class': 'form-control'})
    )
    new_password = forms.CharField(
        label='新的密码',
        min_length=5,
        widget=forms.PasswordInput(attrs={'placeholder': '请输入新密码', 'class': 'form-control'})
    )
    password_again = forms.CharField(
        label='重复密码',
        min_length=5,
        widget=forms.PasswordInput(attrs={'placeholder': '请重复新密码', 'class': 'form-control'})
    )

    def __init__(self, *args, **kwargs):
        if 'user' in kwargs:
            self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

    def clean(self):
        if self.user.is_authenticated:
            self.cleaned_data['username'] = self.user.username
        else:
            raise forms.ValidationError('用户尚未登录')
        new_password = self.cleaned_data['new_password']
        password_again = self.cleaned_data['password_again']
        if not password_again == new_password and new_password != '':
            raise forms.ValidationError('两次输入的密码不同')

    def clean_old_password(self):
        old_password = self.cleaned_data['old_password']
        if not self.user.check_password(old_password):
            raise forms.ValidationError('旧密码不正确')


class ChangeEmailForm(forms.Form):
    email = forms.EmailField(
        label='输入邮箱',
        widget=forms.EmailInput(attrs={'placeholder': '请输入新的邮箱', 'class': 'form-control'})
    )
    verification_code = forms.CharField(
        label='输入验证码',
        required=False,
        widget=forms.TextInput(attrs={'placeholder': '点击"发送验证码"到你输入的邮箱', 'class': 'form-control'})
    )

    def __init__(self, *args, **kwargs):
        if 'request' in kwargs:
            self.request = kwargs.pop('request')
        super().__init__(*args, **kwargs)

    def clean(self):
        if not self.request.user.is_authenticated:
            raise forms.ValidationError('用户尚未登录')
        if self.request.user.email != '':
            raise forms.ValidationError('邮箱已绑定')
        verification_code = self.cleaned_data.get('verification_code', '')
        code = self.request.session.get('bind_email_code')
        if not(code != '' and code == verification_code):
            raise forms.ValidationError('验证码错误')
        return self.cleaned_data

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('邮箱已被绑定')
        return email

    def clean_verification_code(self):
        verification_code = self.cleaned_data.get('verification_code', '').strip()
        if verification_code == '':
            raise forms.ValidationError('验证码不能为空')
        return verification_code


class ForgetPasswordForm(forms.Form):
    email = forms.EmailField(
        label='输入邮箱',
        widget=forms.EmailInput(attrs={'placeholder': '请输入邮箱', 'class': 'form-control'})
    )
    verification_code = forms.CharField(
        label='输入验证码',
        required=False,
        widget=forms.TextInput(attrs={'placeholder': '点击"发送验证码"到你输入的邮箱', 'class': 'form-control'})
    )
    new_password = forms.CharField(
        label='新的密码',
        min_length=5,
        widget=forms.PasswordInput(attrs={'placeholder': '请输入新密码', 'class': 'form-control'})
    )

    def __init__(self, *args, **kwargs):
        if 'request' in kwargs:
            self.request = kwargs.pop('request')
        super().__init__(*args, **kwargs)

    def clean_email(self):
        email = self.cleaned_data.get('email', '')
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError('邮箱尚未绑定')
        return email

    def clean_verification_code(self):
        verification_code = self.cleaned_data.get('verification_code', '').strip()
        code = self.request.session.get('forget_password_code', '')
        if not (code != '' and verification_code == code):
            raise forms.ValidationError('验证码不正确')
        if verification_code == '':
            raise forms.ValidationError('验证码不能为空')
        return verification_code
