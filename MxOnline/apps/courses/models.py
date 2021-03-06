from datetime import datetime

from django.db import models
from organization.models import CourseOrg, Teacher


class Course(models.Model):
    course_org = models.ForeignKey(CourseOrg, verbose_name='组织机构', null=True, blank=True)
    teacher = models.ForeignKey(Teacher, verbose_name='教师', null=True, blank=True)
    name = models.CharField(max_length=100, verbose_name='课程名')
    desc = models.CharField(max_length=300, verbose_name='描述')
    is_banner = models.BooleanField(default=False, verbose_name='是否是轮播图')
    degree = models.CharField(choices=(('cj', '初级'), ('zj', '中级'), ('gj', '高级')), max_length=2, verbose_name='课程难度')
    learn_nums = models.IntegerField(default=0, verbose_name='学习人数')
    dev_nums = models.IntegerField(default=0, verbose_name='收藏人数')
    learn_times = models.IntegerField(default=0, verbose_name='学习时长（分钟数）')
    click_nums = models.IntegerField(default=0, verbose_name='点击数')
    detail = models.TextField(verbose_name='课程详情')
    image = models.ImageField(upload_to='courses/%Y/%m', verbose_name='课程图片', null=True, blank=True)
    course_cate = models.CharField(default='后端开发', max_length=100, verbose_name='课程类型')
    tag = models.CharField(default='', max_length=10, verbose_name='课程标签')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '课程'
        verbose_name_plural = verbose_name

    # 通过外键查找该课程所有章节
    def get_course_lesson(self):
        return self.lesson_set.all().count()

    # 通过外键该课程学习用户
    def get_course_user(self):
        return self.usercourse_set.all()[:5]

    # 获取章节
    def get_lesson(self):
        return self.lesson_set.all()

    def __str__(self):
        return self.name


class Lesson(models.Model):
    course = models.ForeignKey(Course, verbose_name='课程')
    name = models.CharField(max_length=100, verbose_name='章节')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '课程章节'
        verbose_name_plural = verbose_name


class Video(models.Model):
    lesson = models.ForeignKey(Lesson, verbose_name='章节')
    name = models.CharField(max_length=100, verbose_name='视频')
    url = models.CharField(max_length=100, verbose_name='访问地址',default='')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '课程视频'
        verbose_name_plural = verbose_name


class CourseResource(models.Model):
    course = models.ForeignKey(Course, verbose_name='课程')
    name = models.CharField(max_length=100, verbose_name='视频')
    download = models.FileField(upload_to='courses/resource/%Y/%m', verbose_name='资源文件', max_length=100)
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '课程资源'
        verbose_name_plural = verbose_name
