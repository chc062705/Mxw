# -*- coding:utf-8 -*-
from django.conf.urls import url,include

from course.views import CourseListView,CourseDetailView,CoursevideoView,CoursecommentView,AddCoursecommentView,PlayvideoView

urlpatterns = [
    url(r'^list/$',CourseListView.as_view(),name="course_list"),
    url(r'^detail/(?P<course_id>\d+)/$',CourseDetailView.as_view(),name="course_detail"),
    url(r'^ionfo/(?P<course_id>\d+)/$',CoursevideoView.as_view(),name="course_video"),
    url(r'^comment/(?P<course_id>\d+)/$',CoursecommentView.as_view(),name="course_comment"),
    url(r'^addcomment/$',AddCoursecommentView.as_view(),name="Addcourse_comment"),
    url(r'^video/(?P<video_id>\d+)/$',PlayvideoView.as_view(),name="course_play"),

]