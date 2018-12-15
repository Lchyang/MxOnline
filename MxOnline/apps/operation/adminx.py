import xadmin

from .models import UserMessage, UserAsk, UserCourse, UserFavorite, CourseComments


class UserMessageAdmin:
    pass


class UserAskAdmin:
    pass


class UserCourseAdmin:
    pass


class UserFavoriteAdmin:
    pass


class CourseCommentsAdmin:
    pass


xadmin.site.register(UserMessage, UserMessageAdmin)
xadmin.site.register(UserAsk, UserAskAdmin)
xadmin.site.register(UserCourse, UserCourseAdmin)
xadmin.site.register(UserFavorite, UserFavoriteAdmin)
xadmin.site.register(CourseComments, CourseCommentsAdmin)
