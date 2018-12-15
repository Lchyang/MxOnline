from django import forms
from captcha.fields import CaptchaField


class LoginForm(forms.Form):
    # 表单用于检测表单中输入的内容的合法性
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, min_length=6)


class RegisterForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True, min_length=6)
    captcha = CaptchaField()
