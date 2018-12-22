from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser


class UserProfile(AbstractUser):
    nick_name = models.CharField(max_length=50, verbose_name="昵称", default='')
    # blank表示表单验证， null表示数据范畴
    birthday = models.DateField(verbose_name='生日', null=True, blank=True)
    gender = models.CharField(max_length=100, choices=(('male', '男'), ('female', '女')), default='female')
    address = models.CharField(max_length=100, default='')
    mobile = models.CharField(max_length=11, null=True, blank=True)
    # ImageField 需要调用Pillow库
    image = models.ImageField(upload_to='image/%Y/%m', default='image/default.png', max_length=100)

    class Meta:    # 问题这个类什么时候被调用，他的作用是什么？ 在admin界面显示的文字
        '''
        verbose_name:对象的一个易于理解的名称，为单数：
        如果此项没有设置，Django会把类名拆分开来作为自述名，比如CamelCase 会变成camel case，
        verbose_name_plural: 该对象复数形式的名称：
        '''
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username


class EmailVerifyRecord(models.Model):
    code = models.CharField(max_length=50, verbose_name='验证码')
    email = models.EmailField(max_length=30, verbose_name='邮箱')
    send_type = models.CharField('验证码类型', choices=(('register', '注册'),
                                                   ('forget', '找回密码'),
                                                   ('update', '更新邮箱')), max_length=100)
    # datetime.now不能带括号 带括号是实例化时的时间
    send_time = models.DateTimeField('发送时间', default=datetime.now)

    class Meta:
        verbose_name = '邮箱验证码'
        verbose_name_plural = verbose_name

    def __str__(self):
        # xadmin 中默认显示的名称
        return '{}({})'.format(self.code, self.email)


class Banner(models.Model):
    title = models.CharField(max_length=100, verbose_name='标题')
    image = models.ImageField(upload_to='banner/%Y/%m', max_length=100, verbose_name='轮播图')
    url = models.URLField(max_length=100, verbose_name='访问地址')
    index = models.IntegerField(verbose_name='访问顺序')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '轮播图'
        verbose_name_plural = verbose_name
