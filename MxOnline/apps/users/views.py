from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.views.generic.base import View
from django.contrib.auth.hashers import make_password
from django.http.response import JsonResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response

from .models import UserProfile, EmailVerifyRecord, Banner
from operation.models import UserCourse, UserFavorite, UserMessage
from organization.models import CourseOrg
from courses.models import Course, Teacher
from .forms import LoginForm, RegisterForm, ForgetPwdForm, InputPwdForm, ImageUploadForm, \
    RevertPwdForm, UserInfoForm
from utils.send_email import send_register_email
from utils.mixin_utils import LoginRequireMixin


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
                    # 重定向到主页面
                    return HttpResponseRedirect(reverse('index'))
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
        # 通过httpresponse 和 reverse 进行url重定向
        return HttpResponseRedirect(reverse('index'))

        # return render(request, 'index.html')


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

            # 写入注册消息
            message = UserMessage()
            message.user = user_profile.id
            message.message = '欢迎注册'
            message.save()

            send_register_email(user_name, 'register')  # 向用户发送邮件 进入发送邮件的逻辑
            return render(request, 'login.html')  # 邮件发送成功之后返回登录页面
        else:
            return render(request, 'register.html', {'register_form': register_form})


class ForgetPwdView(View):
    # 忘记密码页面
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
    # 进入重置密码页面
    def get(self, request, activate_code):
        all_records = EmailVerifyRecord.objects.filter(code=activate_code)
        if all_records:
            for record in all_records:
                email = record.email
                return render(request, 'password_reset.html', {'email': email})
        else:
            return render(request, 'active.html')


class InputPwdView(View):
    # 重置密码时输入密码
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


class UserInfoView(LoginRequireMixin, View):
    def get(self, request):
        return render(request, 'usercenter-info.html', {})

    def post(self, request):
        user_form = UserInfoForm(request.POST, instance=request.user)
        if user_form.is_valid():
            user_form.save()
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse(user_form.errors)


class ImageUploadView(LoginRequireMixin, View):
    # 上传用户头像
    def post(self, request):
        # 要对request.FILES进行验证，因为图片经过它上传
        upload_form = ImageUploadForm(request.POST, request.FILES)
        if upload_form.is_valid():
            image = upload_form.cleaned_data.get('image', '')
            if image:
                request.user.image = image
                request.user.save()
                return JsonResponse({'status': 'success'})
            else:
                return JsonResponse({'status': 'fail'})
        else:
            return JsonResponse({'status': 'fail'})


class PwdChangeView(LoginRequireMixin, View):
    # 用户个人中心修改密码, 当表单为ajax格式时必须返回json
    def post(self, request):
        input_form = RevertPwdForm(request.POST)
        if input_form.is_valid():
            password1 = request.POST.get('password1', '')
            password2 = request.POST.get('password2', '')
            if password1 != password2:
                return JsonResponse({'status': 'fail', 'msg': '密码不一致'})
            user = request.user
            user.password = make_password(password2)
            user.save()
            return JsonResponse({'status': 'success', 'msg': '密码修改成功'})
        else:
            # 返回表单验证中的错误信息
            return JsonResponse(input_form.errors)


class EmailSendCodeView(LoginRequireMixin, View):
    # 个人中心修改邮箱发送验证码
    def get(self, request):
        email = request.GET.get('email', '')
        exit_email = UserProfile.objects.filter(email=email)
        if exit_email:
            return JsonResponse({'email': '邮箱已经存在'})
        else:
            send_register_email(email, 'update')
            return JsonResponse({'status': 'success', 'msg': '验证码已经发送'})


class EmailUpdateView(LoginRequireMixin, View):
    # 个人中心修改邮箱保存邮箱
    def post(self, request):
        email = request.POST.get('email', '')
        code = request.POST.get('code', '')
        verify_email = EmailVerifyRecord.objects.filter(email=email, code=code)
        if verify_email:
            request.user.email = email
            request.user.save()
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'email': '邮箱更改失败'})


class CoursesView(LoginRequireMixin, View):
    # 个人中心我的课程
    def get(self, request):
        courses = UserCourse.objects.filter(user=request.user)
        return render(request, 'usercenter-mycourse.html', {
            'courses': courses,
        })


class FavoriteCoursesView(LoginRequireMixin, View):
    # 个人中心收藏课程
    def get(self, request):
        fav_courses_id = UserFavorite.objects.filter(user=request.user, fav_type=1)
        fav_id = [fav_course.fav_id for fav_course in fav_courses_id]
        courses = Course.objects.filter(id__in=fav_id)
        return render(request, 'usercenter-fav-course.html', {
            'courses': courses,
        })


class FavoriteTeachersView(LoginRequireMixin, View):
    # 个人中心收藏教师
    def get(self, request):
        fav_teachers_id = UserFavorite.objects.filter(user=request.user, fav_type=3)
        fav_id = [fav_teacher.fav_id for fav_teacher in fav_teachers_id]
        teachers = Teacher.objects.filter(id__in=fav_id)
        return render(request, 'usercenter-fav-teacher.html', {
            'teachers': teachers,
        })


class FavoriteOrgsView(LoginRequireMixin, View):
    # 个人中心收藏机构
    def get(self, request):
        fav_orgs_id = UserFavorite.objects.filter(user=request.user, fav_type=2)
        fav_id = [fav_org.fav_id for fav_org in fav_orgs_id]
        orgs = CourseOrg.objects.filter(id__in=fav_id)
        return render(request, 'usercenter-fav-org.html', {
            'orgs': orgs,
        })


class MessagesView(LoginRequireMixin, View):
    def get(self, request):
        user_messages = UserMessage.objects.filter(user=request.user.id).order_by('-add_time')

        # 用户进入个人消息后清空未读消息记录
        all_unread_messages = UserMessage.objects.filter(user=request.user.id, has_read=False)
        for unread_message in all_unread_messages:
            unread_message.has_read = True
            unread_message.save()

        return render(request, 'usercenter-message.html', {
            'user_messages': user_messages,
        })


class IndexView(View):
    # 主页面
    def get(self, request):
        print(1/0)
        banners = Banner.objects.all().order_by('index')[:5]
        courses = Course.objects.filter(is_banner=False)[:6]
        banner_course = Course.objects.filter(is_banner=True)[:2]
        orgs = CourseOrg.objects.all()[:10]
        return render(request, 'index.html', {
            'banners': banners,
            'courses': courses,
            'banner_course': banner_course,
            'orgs': orgs,
        })


def page_not_found(request):
    # 全局404页面
    response = render_to_response('404.html', {})
    response.status_code = 404
    return response


def page_error(request):
    # 全局500页面
    response = render_to_response('500.html', {})
    response.status_code = 500
    return response

