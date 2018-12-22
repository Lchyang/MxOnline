from django.conf.urls import url, include

from .views import UserInfoView, ImageUploadView, PwdChangeView, EmailSendCodeView, \
    EmailUpdateView, CoursesView, FavoriteCoursesView, FavoriteTeachersView, MessagesView, \
    FavoriteOrgsView


urlpatterns = [
    # 个人中心详情
    url(r'^info/$', UserInfoView.as_view(), name='user_info'),
    # 上传个人头像
    url(r'^image/upload/$', ImageUploadView.as_view(), name='image_upload'),
    # 个人中心密码修改
    url(r'^pwd/change/$', PwdChangeView.as_view(), name='pwd_change'),
    # 修改邮箱发送验证码
    url(r'^email/send_code/$', EmailSendCodeView.as_view(), name='email_send_code'),
    # 保存邮箱
    url(r'^email/update/$', EmailUpdateView.as_view(), name='email_update'),
    # 我的课程
    url(r'^courses/$', CoursesView.as_view(), name='courses'),
    # 我的收藏
    url(r'^favorite/courses$', FavoriteCoursesView.as_view(), name='favorite_courses'),
    url(r'^favorite/teachers$', FavoriteTeachersView.as_view(), name='favorite_teachers'),
    url(r'^favorite/orgs$', FavoriteOrgsView.as_view(), name='favorite_orgs'),
    # 我的消息
    url(r'^messages/$', MessagesView.as_view(), name='messages'),
]