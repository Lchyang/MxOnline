import xadmin
from xadmin import views

from .models import EmailVerifyRecord, Banner


class BaseSetting:
    # xadmin 增加主题
    enable_themes = True
    use_bootswatch = True


class GlobalSetting:
    # xadmin 设置页眉，和页脚
    site_title = '后台管理系统'
    site_footer = '教育在线'
    menu_style = 'accordion'   # 使app状态栏可折叠,要改变app的名字修改apps.py文件，并修改__init__.py


class EmailVerifyRecordAdmin:
    # 在xadmin中显示的字段
    list_display = ['code', 'email', 'send_type', 'send_time']
    # 搜索显示的字段
    search_fields = ['code', 'email', 'send_type']
    # 过滤器中的字段
    list_filter = ['code', 'email', 'send_type', 'send_time']


class BannerAdmin:
    list_display = ['title', 'image', 'url', 'index', 'add_time']
    search_fields = ['title', 'image', 'url', 'index']
    list_filter = ['title', 'image', 'url', 'index', 'add_time']


xadmin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)
xadmin.site.register(Banner, BannerAdmin)
xadmin.site.register(views.BaseAdminView, BaseSetting)     #注册 basesetting
xadmin.site.register(views.CommAdminView, GlobalSetting)   #注册 globalsetting
