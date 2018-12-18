from django.conf.urls import url

from .views import CourseListView, CourseDetailView, CourseVideoView, CourseCommentView, AddCommentView

urlpatterns = [
    # 课程机构首页
    url(r'^list/$', CourseListView.as_view(), name='course_list'),
    url(r'^detail/(?P<course_id>.*)/$', CourseDetailView.as_view(), name='course_detail'),
    url(r'^video/(?P<course_id>.*)/$', CourseVideoView.as_view(), name='course_video'),
    url(r'^comment/(?P<course_id>.*)/$', CourseCommentView.as_view(), name='course_comment'),
    url(r'^add_comment/$', AddCommentView.as_view(), name='add_comment'),
]