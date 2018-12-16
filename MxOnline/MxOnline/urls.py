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
from users.views import LoginView, RegisterView, ActivateRegisterView, ForgetPwdView, RevertPwdView, InputPwdView
from users.views import LogoutView

urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),
    url(r'^captcha/', include('captcha.urls')),
    url(r'^$', TemplateView.as_view(template_name='index.html'), name='index'),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^register/$', RegisterView.as_view(), name='register'),
    # 将active后面的字符获取到传给activate_code变量。
    url(r'active/(?P<activate_code>.*)/$', ActivateRegisterView.as_view(), name = 'register_activate'),
    url(r'^forget/$', ForgetPwdView.as_view(), name='forget_pwd'),
    url(r'revert/(?P<activate_code>.*)/$', RevertPwdView.as_view(), name = 'revert_pwd'),
    url(r'^input/$', InputPwdView.as_view(), name='input_pwd'),

]
