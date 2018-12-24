from django.shortcuts import render
from django.views.generic.base import View
from django.http import JsonResponse

from pure_pagination import Paginator, PageNotAnInteger

from .models import CourseOrg, CityDict, Teacher
from .forms import UserAskForm
from operation.models import UserFavorite, Course


class OrgView(View):
    def get(self, request):
        all_org = CourseOrg.objects.all()
        hot_org = all_org.order_by("-click_nums")[:3]
        all_city = CityDict.objects.all()

        # 取出筛选城市
        city_id = request.GET.get('city', "")
        if city_id:
            all_org = all_org.filter(city_id=int(city_id))

        # 对机构类别进行筛选
        category = request.GET.get('ct', "")
        if category:
            all_org = all_org.filter(category=category)

        sort = request.GET.get('sort', '')
        if sort:
            if sort == 'courses':
                all_org = all_org.order_by('-courses')
            elif sort == 'students':
                all_org = all_org.order_by('-students')

        org_nums = all_org.count()   # 统计数据个数

        # 对课程机构进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # Provide Paginator with the request object for complete querystring generation

        p = Paginator(all_org, 1, request=request)

        orgs = p.page(page)

        return render(request, 'org-list.html', {
            'all_org': orgs,
            'all_city': all_city,
            'org_nums': org_nums,
            'city_id': city_id,
            'category': category,
            'hot_org': hot_org,
            'sort': sort,
        })


class UserAskView(View):
    """
    用户咨询
    """
    def post(self, request):
        ask_form = UserAskForm(request.POST)
        if ask_form.is_valid():
            ask_form.save(commit=True)
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'fail', 'msg': '添加出错'})


class HomePageView(View):
    # 机构首页
    def get(self, request, org_id):
        current_page = 'home'
        course_org = CourseOrg.objects.get(id=int(org_id))
        has_fav = False
        # 在页面中判断用户是否登录，和收藏已显示收藏图标的样式
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=int(2)):
                has_fav = True
        all_courses = course_org.course_set.all()[:3]  # 通过外键取出所有子表数据
        all_teachers = course_org.teacher_set.all()[:1]
        return render(request, 'org-detail-homepage.html', {
            'all_courses': all_courses,
            'all_teachers': all_teachers,
            'course_org': course_org,
            'current_page': current_page,
            'has_fav': has_fav,
        })


class CourseView(View):
    # 机构课程
    def get(self, request, course_id):
        current_page = 'course'
        course_org = CourseOrg.objects.get(id=int(course_id))
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=int(2)):
                has_fav = True
        all_courses = course_org.course_set.all()
        return render(request, 'org-detail-course.html', {
            'all_courses': all_courses,
            'course_org': course_org,
            'current_page': current_page,
            'has_fav': has_fav,
        })


class DescView(View):
    # 机构描述
    def get(self, request, course_id):
        current_page = 'desc'
        course_org = CourseOrg.objects.get(id=int(course_id))
        return render(request, 'org-detail-desc.html', {
            'course_org': course_org,
            'current_page': current_page,
        })


class TeacherView(View):
    # 机构教师
    def get(self, request, course_id):
        current_page = 'teacher'
        course_org = CourseOrg.objects.get(id=int(course_id))
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=int(2)):
                has_fav = True
        all_teachers = course_org.teacher_set.all()
        return render(request, 'org-detail-teachers.html', {
            'all_teachers': all_teachers,
            'course_org': course_org,
            'current_page': current_page,
            'has_fav': has_fav,
        })


class AddFavView(View):
    # 添加收藏逻辑
    def post(self, request):
        fav_id = request.POST.get('fav_id', 0)
        fav_type = request.POST.get('fav_type', 0)
        user = request.user
        # 判断用户是否登录，不登录不能收藏
        if not user.is_authenticated():
            return JsonResponse({'status': 'fail', 'msg': '用户未登录'})
        # 判断是否已经收藏，已经收藏则取消收藏
        exit_fav = UserFavorite.objects.filter(user=user, fav_id=int(fav_id), fav_type=int(fav_type))
        if exit_fav:
            exit_fav.delete()
            if int(fav_type) == 1:
                course = Course.objects.get(id=int(fav_id))
                course.dev_nums -= 1
                if course.dev_nums < 0:
                    course.dev_nums = 0
                course.save()
            if int(fav_type) == 2:
                course_org = CourseOrg.objects.get(id=int(fav_id))
                course_org.dev_nums -= 1
                if course_org.dev_nums < 0:
                    course_org.dev_nums = 0
                course_org.save()
            if int(fav_type) == 3:
                teacher = Teacher.objects.get(id=int(fav_id))
                teacher.dev_nums -= 1
                if teacher.dev_nums < 0:
                    teacher.dev_nums = 0
                teacher.save()

            return JsonResponse({'status': 'success', 'msg': '取消收藏成功'})
        else:
            # 如果没有收藏则把数据保存到数据库，字段要填写完整。
            user_fav = UserFavorite()
            if int(fav_type) > 0 and int(fav_id) > 0:
                user_fav.user = user
                user_fav.fav_id = int(fav_id)
                user_fav.fav_type = int(fav_type)
                user_fav.save()
                # 数据库收藏数加一
                if int(fav_type) == 1:
                    course = Course.objects.get(id=int(fav_id))
                    course.dev_nums += 1
                    if course.dev_nums < 0:
                        course.dev_nums = 0
                    course.save()
                if int(fav_type) == 2:
                    course_org = CourseOrg.objects.get(id=int(fav_id))
                    course_org.dev_nums += 1
                    if course_org.dev_nums < 0:
                        course_org.dev_nums = 0
                    course_org.save()
                if int(fav_type) == 3:
                    teacher = Teacher.objects.get(id=int(fav_id))
                    teacher.dev_nums += 1
                    if teacher.dev_nums < 0:
                        teacher.dev_nums = 0
                    teacher.save()
                return JsonResponse({'status': 'success', 'msg': '收藏成功'})
            else:
                return JsonResponse({'status': 'fail', 'msg': '收藏出错'})


class TeacherListView(View):
    def get(self, request):
        teachers = Teacher.objects.all()
        hot_teachers = teachers.order_by('-click_nums')[:3]
        sort = request.GET.get('sort', '')

        if sort:
            if sort == 'hot':
                teachers = teachers.order_by('-click_nums')

        # 对讲师列表进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # Provide Paginator with the request object for complete querystring generation

        p = Paginator(teachers, 2, request=request)
        teachers = p.page(page)

        return render(request, 'teachers-list.html', {
            'teachers': teachers,
            'sort': sort,
            'hot_teachers': hot_teachers,
        })


class TeacherDetailView(View):
    # 教师详情页
    def get(self, request, teacher_id):
        teacher = Teacher.objects.get(id=teacher_id)
        teacher.click_nums += 1
        teacher.save()
        courses = Course.objects.filter(teacher=teacher)
        hot_teachers = Teacher.objects.all().order_by('-click_nums')[:3]

        teacher_fav = False
        org_fav = False

        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=teacher.id, fav_type=int(3)):
                teacher_fav = True
            if UserFavorite.objects.filter(user=request.user, fav_id=teacher.id, fav_type=int(2)):
                org_fav = True

        return render(request, 'teacher-detail.html', {
            'teacher': teacher,
            'courses': courses,
            'hot_teachers': hot_teachers,
            'teacher_fav': teacher_fav,
            'org_fav': org_fav,
        })
