from django import forms
from django.contrib import auth
from django.contrib.auth.models import User

class LoginForm(forms.Form):
    username = forms.CharField(label="账号",
                               widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入账号'}))
    password = forms.CharField(label="密码",
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '请输入密码'}))

    def clean(self):
        '''
        进行账号验证
        :return:cleaned_data
        '''
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        user = auth.authenticate(username=username, password=password)
        if user is None:
            raise forms.ValidationError('用户名或密码不正确，登录失败！')
        else:
            self.cleaned_data['user'] = user
        return self.cleaned_data

class RegisterForm(forms.Form):
    username = forms.CharField(label="账号",min_length=6, max_length=20,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入6-20位的账号'}))
    email = forms.EmailField(label="邮箱",
                               widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': '请输入邮箱'}))

    password = forms.CharField(label="密码", min_length=6,
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '请输入密码'}))
    password_repeat = forms.CharField(label="确认密码", min_length=6,
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '确认密码'}))

    def clean_username(self):
        # 验证账号是否存在
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('该账号已被注册，请重新输入')
        return username

    def clean_email(self):
        # 验证邮箱是否存在
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('该邮箱已被注册，请重新输入')
        return email

    def clean_password_repeat(self):
        password = self.cleaned_data['password']
        password_repeat = self.cleaned_data['password_repeat']
        if password != password_repeat:
            raise forms.ValidationError('两次输入密码不一致')

        elif password.isdigit() or password.isalpha():
            # 密码全由数字或字母组成，不安全
            raise forms.ValidationError('密码至少应为数字加字母的组合')

        else:
            return password_repeat
