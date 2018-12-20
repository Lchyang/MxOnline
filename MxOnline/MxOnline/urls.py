"""MxOnline URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
import xadmin

from django.conf.urls import url, include
from django.views.generic import TemplateView
from django.views.static import serve
from MxOnline.settings import MEDIA_ROOT

from users.views import LoginView, LogoutView, RegisterView, ActivateRegisterView, \
    ForgetPwdView, RevertPwdView, InputPwdView


urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),
    # 配置验证码
    url(r'^captcha/', include('captcha.urls')),
    # 直接返回模板不用通过view
    url(r'^$', TemplateView.as_view(template_name='index.html'), name='index'),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^register/$', RegisterView.as_view(), name='register'),
    # 获取url中变量，将active后面的字符获取到传给activate_code变量。
    url(r'active/(?P<activate_code>.*)/$', ActivateRegisterView.as_view(), name = 'register_activate'),
    url(r'^forget/$', ForgetPwdView.as_view(), name='forget_pwd'),
    url(r'revert/(?P<activate_code>.*)/$', RevertPwdView.as_view(), name = 'revert_pwd'),
    # 输入重置密码
    url(r'^input/$', InputPwdView.as_view(), name='input_pwd'),

    url(r'^org/', include('organization.urls', namespace='org')),
    url(r'^course/', include('courses.urls', namespace='courses')),
    url(r'^teachers/', include('organization.urls', namespace='teachers')),

    # 配置上传文件的访问处理函数
    url(r'^media/(?P<path>.*)$', serve, {'document_root': MEDIA_ROOT})



]
