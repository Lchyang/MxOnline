from datetime import datetime

from django.db import models

# Create your models here.

class Course(models.Model):
    name = models.CharField(max_length=100, verbose_name='课程名')
    desc = models.CharField(max_length=300, verbose_name='描述')
    degree = models.CharField(choices=(('cj', '初级'), ('zj', '中级'), ('gj', '高级')), max_length=2, verbose_name='课程难度')
    learn_nums = models.IntegerField(default=0, verbose_name='学习人数')
    dev_nums = models.IntegerField(default=0, verbose_name='收藏人数')
    learn_times = models.IntegerField(default=0, verbose_name='学习时长（分钟数）')
    click_nums = models.IntegerField(default=0, verbose_name='点击数')
    detail = models.TextField(verbose_name='课程详情')
    image = models.ImageField(upload_to='courses/%Y/%m', verbose_name='课程图片')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '课程'
        verbose_name_plural = verbose_name

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
    lesson = models.ForeignKey(Course, verbose_name='章节')
    name = models.CharField(max_length=100, verbose_name='视频')
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
