import xadmin

from .models import CityDict, CourseOrg, Teacher

class CityDictAdmin:
    list_display = ['name', 'desc', 'add_time']
    search_fields = ['name', 'desc',]
    list_filter = ['name', 'desc', 'add_time']


class CourseOrgAdmin:
    list_display = ['name', 'desc', 'click_nums', 'address', 'city', 'add_time']
    search_fields = ['name', 'desc', 'click_nums', 'address', 'city',]
    list_filter = ['name', 'desc', 'click_nums', 'address', 'city', 'add_time']


class TeacherAdmin:
    list_display = ['org', 'name', 'work_years', 'points', 'work_position']
    search_fields = ['org', 'name', 'work_years', 'points', 'work_position']
    list_filter =  ['org', 'name', 'work_years', 'points', 'work_position']


xadmin.site.register(CityDict, CityDictAdmin)
xadmin.site.register(CourseOrg, CourseOrgAdmin)
xadmin.site.register(Teacher, TeacherAdmin)
