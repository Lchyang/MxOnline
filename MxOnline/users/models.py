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

    class Meta:    # 问题这个类什么时候被调用，他的作用是什么？
        '''
        verbose_name:对象的一个易于理解的名称，为单数：
        如果此项没有设置，Django会把类名拆分开来作为自述名，比如CamelCase 会变成camel case，
        verbose_name_plural: 该对象复数形式的名称：
        '''
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username
