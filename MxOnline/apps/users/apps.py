from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = 'users'
    # 设置xadmin中的app名称
    verbose_name = '用户信息'
