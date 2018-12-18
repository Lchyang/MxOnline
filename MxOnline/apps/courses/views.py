from pure_pagination import Paginator, PageNotAnInteger

from django.shortcuts import render
from django.views.generic.base import View
from django.http import JsonResponse

from .models import Course, CourseResource
from operation.models import UserFavorite, CourseComments, UserCourse
from utils.mixin_utils import LoginRequireMixin


class CourseListView(View):
    def get(self, request):
        all_courses = Course.objects.all().order_by('-add_time')
        hot_courses = Course.objects.all().order_by('-click_nums')[:3]

        # 根据功能筛选
        sort = request.GET.get('sort', '')
        if sort:
            if sort == 'hot':
                all_courses = all_courses.order_by('-click_nums')
            elif sort == 'learn_nun':
                all_courses = all_courses.order_by('-learn_nums')

        # 对课程列表进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # Provide Paginator with the request object for complete querystring generation

        p = Paginator(all_courses, 3, request=request)

        courses = p.page(page)
        return render(request, 'course-list.html', {
            'all_courses': courses,
            'hot_courses': hot_courses,
            'sort': sort,
        })


class CourseDetailView(View):
    def get(self, request, course_id):
        courses = Course.objects.get(id=int(course_id))
        # 增加点击数
        courses.click_nums += 1
        courses.save()

        # 相关课程推荐
        tag = courses.tag
        if tag:
            course_tag = Course.objects.filter(tag=tag)[:1]
        else:
            course_tag = []

        has_course_fav = False
        has_org_fav = False
        # 在页面中判断用户是否登录，和收藏已显示收藏图标的样式
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=courses.id, fav_type=1):
                has_course_fav = True
            if UserFavorite.objects.filter(user=request.user, fav_id=courses.course_org.id, fav_type=2):
                has_org_fav = True
        return render(request, 'course-detail.html', {
            'courses': courses,
            'course_tag': course_tag,
            'has_course_fav': has_course_fav,
            'has_org_fav': has_org_fav,
        })


class CourseVideoView(LoginRequireMixin, View):
    # 课程章节和视频页面信息
    def get(self, request, course_id):
        courses = Course.objects.get(id=int(course_id))
        course_resources = CourseResource.objects.filter(course=courses)

        learn_course = UserCourse.objects.filter(user=request.user, course=courses)
        if not learn_course:
            course = UserCourse()
            course.user = request.user
            course.course = courses
            course.save()

        user_courses = UserCourse.objects.filter(course=courses)  # 过滤出相同course的usercourse对象
        user_id = [user_course.user.id for user_course in user_courses]  # 获取所有usercourse对象中user的id
        # user_id__in表示可以遍历user_id中的元素然后进行查找, 根据用户找到所有usercourse对象
        all_user_courses =  UserCourse.objects.filter(user_id__in=user_id)
        # 根据所有usercourse对象找到所有course的ID
        course_ids = [user_course.course.id for user_course in all_user_courses]
        # 取出所有的course
        all_courses = Course.objects.filter(id__in=course_ids).order_by('-click_nums')

        return render(request, 'course-video.html', {
            'courses': courses,
            'course_resources': course_resources,
            'all_courses': all_courses,
        })


class CourseCommentView(LoginRequireMixin, View):
    # 课程评论页面信息
    def get(self, request, course_id):
        courses = Course.objects.get(id=int(course_id))
        course_resources = CourseResource.objects.filter(course=courses)
        all_comments = CourseComments.objects.filter(course=courses).order_by('-add_time')
        return render(request, 'course-comment.html', {
            'courses': courses,
            'course_resources': course_resources,
            'all_comments': all_comments,
        })


class AddCommentView(View):
    # 用户添加评论,和收藏的逻辑类似
    def post(self, request):
        course_id = request.POST.get('course_id', 0)
        comment = request.POST.get('comments', '')
        user = request.user
        if not user.is_authenticated():
            return JsonResponse({'status': 'fail', 'msg': '用户未登录'})
        else:
            comment_db = CourseComments()
            # 注意这要做一下判断，防止无用信息存入数据库
            if int(course_id) > 0 and comment:
                comment_db.user = user
                comment_db.course = Course.objects.get(id=int(course_id))
                comment_db.comments = comment
                comment_db.save()
                return JsonResponse({'status': 'success', 'msg': '评论成功'})
            else:
                return JsonResponse({'status': 'fail', 'msg': '评论成功'})
