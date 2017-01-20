# -*- coding:utf-8 -*-
import xadmin
from .models import *


class CityAdmin(object):
    pass
xadmin.site.register(City,CityAdmin)

class CourseorgAdmin(object):
    pass
xadmin.site.register(Courseorg,CourseorgAdmin)

class TeacherAdmin(object):
    pass
xadmin.site.register(Teacher,TeacherAdmin)