from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.views.generic.base import View
from django.contrib.auth.hashers import make_password

from .models import UserProfile
from .forms import LoginForm, RegisterForm


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
                # login将用户登录
                login(request, user)
                return render(request, 'index.html')
            else:
                return render(request, 'login.html', {'msg': '用户名或密码错误'})
        else:
            #将表单信息传给模板，用于错误处理
            return render(request, 'login.html', {'login_form': login_form})


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


class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()
        return render(request, 'register.html', {'register_form': register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_name = request.POST.get('username', '')  # 获取username(request中的参数）
            pass_word = request.POST.get('password', '')  # 获取password
            user_profile = UserProfile()
            user_profile.username = user_name
            user_profile.email = user_name
            user_profile.password = make_password(pass_word)
            user_profile.save()
