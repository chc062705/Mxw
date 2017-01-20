# -*- coding:utf-8 -*-
from django.shortcuts import render
from django.views.generic import View
from course.models import Course,CourseResource,Video
from operation.models import UserFavorite,CourseComments,UserCourse
from django.http import HttpResponse
from django.db.models import Q
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from utils.minxin_until import LoginRequiredMinxin
# Create your views here.


class CourseListView(View):
    def get(self,request):
        all_coirse=Course.objects.all().order_by("-add_time")
        hot_course=all_coirse.order_by("-click_nums")[:3]

        sort = request.GET.get('sort', "")
        key_word=request.GET.get('keywords',"")
        if key_word:
            all_coirse=all_coirse.filter(Q(name__icontains=key_word)|Q(desc__icontains=key_word)|Q(detail__icontains=key_word))
        if sort=="students":
            all_coirse=all_coirse.order_by("-students")
        elif sort=="hot":
            all_coirse=all_coirse.order_by("-click_nums")
        try:
             page = request.GET.get('page', 1)
        except PageNotAnInteger:
             page = 1
        p = Paginator(all_coirse,4, request=request)

        courses = p.page(page)
        return render(request,"course-list.html",{
            "course":courses,
            "sort":sort,
            "hot_course":hot_course
        })

class CourseDetailView(View):
    def get(self,request,course_id):
        course=Course.objects.get(id=course_id)
        course.click_nums+=1
        course.save()
        tag=course.tag
        fav_course=False
        fav_org=False
        if  request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user,fav_id=course.id,fav_type=1):
                fav_course=True
            if UserFavorite.objects.filter(user=request.user,fav_id=course.course_org.id,fav_type=2):
                fav_org=True
        if tag:
            relate_course=Course.objects.filter(tag=tag)[:1]
        else:
            relate_course=[]

        return render(request,"course-detail.html",{
            "course":course,
            "relate_course":relate_course,
            "fav_org":fav_org,
            "fav_course":fav_course

        })
class CoursevideoView(LoginRequiredMinxin,View):
    def get(self,request,course_id):
        course=Course.objects.get(id=course_id)
        user_courses=UserCourse.objects.filter(course=course)
        usercourse=UserCourse.objects.filter(user=request.user,course=course)
        if not usercourse:
            course.students+=1
            course.save()
            user_course=UserCourse(user=request.user,course=course)
            user_course.save()
        user_ids=[user_course.user.id for user_course in user_courses]
        all_user_courses=UserCourse.objects.filter(user_id__in=user_ids)
        relate_course_ids=[user_course.course.id for user_course in user_courses]
        relate_course_aaa=Course.objects.filter(id__in=relate_course_ids)[:3]
        course.click_nums+=1
        course.save()
        tag=course.tag
        fav_course=False
        fav_org=False
        if  request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user,fav_id=course.id,fav_type=1):
                fav_course=True
            if UserFavorite.objects.filter(user=request.user,fav_id=course.course_org.id,fav_type=2):
                fav_org=True
        if tag:
            relate_course=Course.objects.filter(tag=tag)[:1]
        else:
            relate_course=[]
        course_resoue=CourseResource.objects.filter(course=course)

        return render(request,"course-video.html",{
            "course":course,
            "relate_course":relate_course,
            "fav_org":fav_org,
            "fav_course":fav_course,
            "course_resoue":course_resoue,
            "relate_course_aaa":relate_course_aaa

        })
class CoursecommentView(LoginRequiredMinxin,View):
    def get(self,request,course_id):
        course=Course.objects.get(id=course_id)
        comment=CourseComments.objects.filter(course_id=course_id).order_by("-add_time")
        return render(request,"course-comment.html",{
            "course":course,
            "comment":comment
        })
class AddCoursecommentView(View):
    def post(self,request):
        if not request.user.is_authenticated():
             return HttpResponse('{"status":"fail", "msg":"用户未登录"}', content_type='application/json')
        course_id=request.POST.get("course_id",0)
        comment=request.POST.get("comments","")
        if course_id> 0 and comment:
            course_comments=CourseComments()
            course=Course.objects.get(id=course_id)
            course_comments.course=course
            course_comments.comments=comment
            course_comments.user=request.user
            course_comments.save()
            return HttpResponse('{"status":"success", "msg":"添加成功"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail", "msg":"添加出错"}', content_type='application/json')
class PlayvideoView(LoginRequiredMinxin,View):
    def get(self,request,video_id):
        video=Video.objects.get(id=video_id)
        course=video.lesson.course
        user_courses=UserCourse.objects.filter(course=course)
        usercourse=UserCourse.objects.filter(user=request.user,course=course)
        if not usercourse:
            user_course=UserCourse(user=request.user,course=course)
            course.students+=1
            course.save()
            user_course.save()
        user_ids=[user_course.user.id for user_course in user_courses]
        all_user_courses=UserCourse.objects.filter(user_id__in=user_ids)
        relate_course_ids=[user_course.course.id for user_course in user_courses]
        relate_course_aaa=Course.objects.filter(id__in=relate_course_ids)[:3]
        course.click_nums+=1
        course.save()
        tag=course.tag
        fav_course=False
        fav_org=False
        if  request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user,fav_id=course.id,fav_type=1):
                fav_course=True
            if UserFavorite.objects.filter(user=request.user,fav_id=course.course_org.id,fav_type=2):
                fav_org=True
        if tag:
            relate_course=Course.objects.filter(tag=tag)[:1]
        else:
            relate_course=[]
        course_resoue=CourseResource.objects.filter(course=course)

        return render(request,"course-pp.html",{
            "course":course,
            "relate_course":relate_course,
            "fav_org":fav_org,
            "fav_course":fav_course,
            "course_resoue":course_resoue,
            "relate_course_aaa":relate_course_aaa,
            "video":video

        })




