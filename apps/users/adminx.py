# -*- coding:utf-8 -*-
import xadmin
from .models import *


# class UserProfileAdmin(object):
#     pass
# xadmin.site.register(UserProfile,UserProfileAdmin)

class  EmailVerifyRecordAdmin(object):
    pass
xadmin.site.register( EmailVerifyRecord, EmailVerifyRecordAdmin)

class BannerAdmin(object):
    pass
xadmin.site.register(Banner,BannerAdmin)

