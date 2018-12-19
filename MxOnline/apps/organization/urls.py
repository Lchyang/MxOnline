from django.conf.urls import url, include

from .views import OrgView, UserAskView, HomePageView, CourseView, DescView, TeacherView, AddFavView
from .views import TeacherListView, TeacherDetailView

urlpatterns = [
    # 课程机构首页
    url(r'^list/$', OrgView.as_view(), name='org_list'),
    url(r'^add_ask/$', UserAskView.as_view(), name='add_ask'),
    url(r'^home/(?P<org_id>\d+)/$', HomePageView.as_view(), name='home'),
    url(r'^course/(?P<course_id>\d+)/$', CourseView.as_view(), name='course'),
    url(r'^desc/(?P<course_id>\d+)/$', DescView.as_view(), name='desc'),
    url(r'^teacher/(?P<course_id>\d+)/$', TeacherView.as_view(), name='teacher'),
    # 添加用户收藏
    url(r'^add_fav/$', AddFavView.as_view(), name='add_fav'),

    url(r'^teacher/list/$', TeacherListView.as_view(), name='teacher_list'),
    url(r'^teacher/detail/(?P<teacher_id>\d+)/$', TeacherDetailView.as_view(), name='teacher_detail'),
]