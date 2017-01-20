# -*- coding:utf-8 -*-
import xadmin
from .models import *


class UserAskAdmin(object):
    pass
xadmin.site.register(UserAsk,UserAskAdmin)

class CourseCommentsAdmin(object):
    pass
xadmin.site.register(CourseComments,CourseCommentsAdmin)

class UserFavoriteAdmin(object):
    pass
xadmin.site.register(UserFavorite,UserFavoriteAdmin)

class UserMassageAdmin(object):
    pass
xadmin.site.register(UserMassage,UserMassageAdmin)

class UserCourseAdmin(object):
    pass
xadmin.site.register(UserCourse,UserCourseAdmin)