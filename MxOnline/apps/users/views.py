from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.views.generic.base import View
from django.contrib.auth.hashers import make_password

from .models import UserProfile, EmailVerifyRecord
from .forms import LoginForm, RegisterForm, ForgetPwdForm, InputPwdForm
from utils.send_email import send_register_email


class CustomBackend(ModelBackend):
    '''
    在user_login中只能通过用户名进行登录，如果想用邮箱登录需要重载ModelBackend类中的authenticate 方法
    在setting.py 中添加：
    AUTHENTICATION_BACKENDS = (
        'user.views.CustomBackend',
    )
    '''
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # Q用于数据库查询的操作 | 代表或 ，代表 and
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
        except Exception:
            return None


class LoginView(View):
    def get(self, request):
        return render(request, 'login.html', {})

    def post(self, request):
        # 实例化表单
        login_form = LoginForm(request.POST)
        # 检测表单是否合法
        if login_form.is_valid():
            user_name = request.POST.get('username', '')  # 获取username(request中的参数）
            pass_word = request.POST.get('password', '')  # 获取password
            # 此函数验证用户名密码是否正确，错误返回none 参数以键值方式传递,
            # 如果重载了此函数执行重载的函数进行逻辑处理
            user = authenticate(username=user_name, password=pass_word)
            if user:
                # 如果此时用户只是注册了没有验证is_active为false不能登录返回错误
                if user.is_active:
                    # login将用户登录
                    login(request, user)
                    return render(request, 'index.html')
                else:
                    return render(request, 'login.html', {'msg': '用户未激活'})
            else:
                return render(request, 'login.html', {'msg': '用户名或密码错误'})
        else:
            #将表单信息传给模板，用于错误处理
            return render(request, 'login.html', {'login_form': login_form})


class LogoutView(View):
    def get(self, request):
        logout(request)
        return render(request, 'index.html')


# 基于函数视图
'''
def user_login(request):
    # 登录表单提交后检测post方法
    if request.method == 'POST':
        user_name = request.POST.get('username', '') #获取username(request中的参数）
        pass_word = request.POST.get('password', '') #获取password
        # 此函数验证用户名密码是否正确，错误返回none 参数以键值方式传递,
        # 如果重载了此函数执行重载的函数进行逻辑处理
        user = authenticate(username=user_name, password=pass_word)
        if user:
            # login将用户登录
            login(request, user)
            return render(request, 'index.html')
        else:
            return render(request, 'login.html', { 'msg': '用户名或密码错误'})
    elif request.method == 'GET':
        # 如果是get请求返回主界面
        return render(request, 'login.html', {})
'''


# 用户验证类
class ActivateRegisterView(View):
    # 用户访问一个激活的链接会将随机生成的字符串通过url（request请求）带回来，
    # 通过随机字符串找到邮箱，通过邮箱找到这个用户，把is_active设为true激活成功。
    def get(self, request, activate_code):
        all_records = EmailVerifyRecord.objects.filter(code=activate_code)
        if all_records:
            for records in all_records:
                email = records.email
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
            return render(request, 'login.html')
        else:
            return render(request, 'active.html')



class RegisterView(View):
    # 用户注册逻辑
    def get(self, request):
        # 访问URL时返回register.html页面
        register_form = RegisterForm()
        return render(request, 'register.html', {'register_form': register_form})

    def post(self, request):
        # 输入数据时form表单进行格式检查
        register_form = RegisterForm(request.POST)
        # 如果表单验证合法
        if register_form.is_valid():
            user_name = request.POST.get('email', '')  # 获取username(request中的参数）
            if UserProfile.objects.filter(email=user_name):  # 检测用户是否已经存在
                return render(request, 'register.html', {'msg': '用户已经存在'})
            pass_word = request.POST.get('password', '')  # 获取password
            user_profile = UserProfile()
            user_profile.username = user_name  # 从表单中拿到的数据保存在user_profile数据库中
            user_profile.email = user_name   # 因为用邮箱登录所以用户名也保存成邮箱
            user_profile.password = make_password(pass_word)  # 密码用密文保存，需要调用make_password()方法
            user_profile.is_active = False  # 此时只是注册用户没有通过邮箱激活所以is_activate()设为false
            user_profile.save()

            send_register_email(user_name, 'register')  # 向用户发送邮件 进入发送邮件的逻辑
            return render(request, 'login.html')  # 邮件发送成功之后返回登录页面
        else:
            return render(request, 'register.html', {'register_form': register_form})


class ForgetPwdView(View):
    def get(self, request):
        forget_form = ForgetPwdForm()
        return render(request, 'forgetpwd.html', {'forget_form': forget_form})

    def post(self, request):
        forget_form = ForgetPwdForm(request.POST)
        if forget_form.is_valid():
            user_name = request.POST.get('email', '')  # 获取username(request中的参数）
            if UserProfile.objects.filter(email=user_name):
                send_register_email(user_name, 'forget')
                return render(request, 'success_send.html')
            else:
                return render(request, 'forgetpwd.html', {'forget_form': forget_form, 'msg': '用户没有注册'})
        else:
            return render(request, 'forgetpwd.html', {'forget_form': forget_form})


class RevertPwdView(View):
    def get(self, request, activate_code):
        all_records = EmailVerifyRecord.objects.filter(code=activate_code)
        if all_records:
            for record in all_records:
                email = record.email
                return render(request, 'password_reset.html', {'email': email})
        else:
            return render(request, 'active.html')


class InputPwdView(View):
    def post(self, request):
        input_form = InputPwdForm(request.POST)
        if input_form.is_valid():
            email = request.POST.get('email', '')
            password1 = request.POST.get('password1', '')
            password2 = request.POST.get('password2', '')
            if password1 != password2:
                return render(request, 'password_reset.html', {'email': email, 'msg': '密码不一致'})
            user = UserProfile.objects.get(email=email)
            user.password = make_password(password2)
            user.save()
            return render(request, 'login.html', {'msg': '密码修改成功请重新登录'})
        else:
            email = request.POST.get('email', '')
            return render(request, 'password_reset.html', {'input_form': input_form, 'email': email})
