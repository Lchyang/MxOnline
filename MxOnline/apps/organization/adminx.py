import xadmin

from .models import CityDict, CourseOrg, Teacher

class CityDictAdmin:
    pass


class CourseOrgAdmin:
    pass


class TeacherAdmin:
    pass


xadmin.site.register(CityDict, CityDictAdmin)
xadmin.site.register(CourseOrg, CourseOrgAdmin)
xadmin.site.register(Teacher, TeacherAdmin)
