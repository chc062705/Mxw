# -*- coding:utf-8 -*-
from django.conf.urls import url,include

from organization.views import OrgView, AddUserAskView,OrgHomeView,OrgCourseView,OrgdescView,OrgtteacherView,AddFavView,teacherlistView,teacherdetailView

urlpatterns = [
    url(r'^list/$',OrgView.as_view(),name="org_list"),
    url(r'^add_ask/$', AddUserAskView.as_view(),name="addask"),
    url(r'^home/(?P<org_id>\d+)/$', OrgHomeView.as_view(), name="org_home"),
    url(r'^OrgCourse/(?P<org_id>\d+)/$', OrgCourseView.as_view(), name="org_course"),
    url(r'^Orgdesc/(?P<org_id>\d+)/$', OrgdescView.as_view(), name="org_desc"),
    url(r'^Orgteacher/(?P<org_id>\d+)/$', OrgtteacherView.as_view(), name="org_teacher"),
    #机构收藏
    url(r'^add_fav/$', AddFavView.as_view(),name="addfav"),
    url(r'^teacher/list/$', teacherlistView.as_view(), name="teacher_list"),
    url(r'^teacher/detali/(?P<teacher_id>\d+)/$',teacherdetailView.as_view(), name="detail_teacher"),

]