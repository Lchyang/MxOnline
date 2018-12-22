from django import forms
from captcha.fields import CaptchaField

from .models import UserProfile


class LoginForm(forms.Form):
    # 表单用于检测表单中输入的内容的合法性
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, min_length=6)


class RegisterForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True, min_length=6)
    # 用于验证码的验证
    captcha = CaptchaField()


class ForgetPwdForm(forms.Form):
    email = forms.EmailField(required=True)
    # 用于验证码的验证
    captcha = CaptchaField()


class InputPwdForm(forms.Form):
    password1 = forms.CharField(required=True, min_length=6)
    password2 = forms.CharField(required=True, min_length=6)
    email = forms.EmailField(required=True)


class ImageUploadForm(forms.ModelForm):
    # 上传用户头像表单
    class Meta:
        model = UserProfile
        fields = ['image']


class RevertPwdForm(forms.Form):
    # 个人中心修改密码
    password1 = forms.CharField(required=True, min_length=6)
    password2 = forms.CharField(required=True, min_length=6)


class UserInfoForm(forms.ModelForm):
    # 上传用户头像表单
    class Meta:
        model = UserProfile
        fields = ['nick_name', 'birthday', 'gender', 'address', 'mobile', 'email']
