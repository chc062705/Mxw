# -*- coding:utf-8 -*-
from django.shortcuts import render
from django.views.generic import View
from organization.models import Courseorg,City,Teacher
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from organization.froms import UserAskForm
from operation.models import UserFavorite
from django.http import HttpResponse
from django.db.models import Q
from course.models import *
from rest_framework import status
# Create your views here.


class OrgView(View):
    def get(self,request):
        #课程机构
        all_org=Courseorg.objects.all()
        hot_org=all_org.order_by("-click_nums")[:3]
        #城市
        all_city=City.objects.all()
        key_word=request.GET.get('keywords',"")
        if key_word:
            all_org=all_org.filter(Q(name__icontains=key_word)|Q(desc__icontains=key_word))
        city_id = request.GET.get('city', "")
        if city_id:
            all_org=all_org.filter(city_id=int(city_id))
        category_id = request.GET.get('ct', "")
        if category_id:
            all_org=all_org.filter(category=category_id)
        sort = request.GET.get('sort', "")
        if sort=="students":
            all_org=all_org.order_by("-students")
        elif sort=="courses":
            all_org=all_org.order_by("-course_nums")

#对机构进行分页
        try:
             page = request.GET.get('page', 1)
        except PageNotAnInteger:
             page = 1
        p = Paginator(all_org,3, request=request)

        orgs = p.page(page)
        org=all_org.count()


        return  render(request,"org-list.html",{
            "org":orgs,
            "all_city":all_city,
            "num":org,
            "city_id":city_id,
            "ct":category_id,
            "hot_org":hot_org,
            "sort":sort
        })


class AddUserAskView(View):
    def post(self,request):
         userask_form=UserAskForm(request.POST)
         if userask_form.is_valid():
             user_ask=userask_form.save(commit=True)
             return HttpResponse('{"status":"success"}', content_type='application/json')
         else:
             return HttpResponse('{"status":"fail", "msg":"添加出错"}', content_type='application/json')

class OrgHomeView(View):
       #机构首页
       def get(self, request,org_id):
           current_page="Home"
           course_org=Courseorg.objects.get(id=int(org_id))
           course_org.click_nums+=1
           course_org.save()
           all_course=course_org.course_set.all()[:3]
           all_teacher=course_org.teacher_set.all()[:1]
           return render(request,"org-detail-homepage.html",{
               'all_course':all_course,
               'all_teacher':all_teacher,
               'course_org':course_org,
               "current_page":current_page
           })


class OrgCourseView(View):
       #机构首页
       def get(self, request,org_id):
           current_page="Course"
           course_org=Courseorg.objects.get(id=int(org_id))
           all_course=course_org.course_set.all()[:3]
           all_teacher=course_org.teacher_set.all()[:1]
           #对机构进行分页
           try:
                 page = request.GET.get('page', 1)
           except PageNotAnInteger:
                 page = 1
           p = Paginator(all_course,3, request=request)
           orgs = p.page(page)
           return render(request,"org-detail-course.html",{
               'all_course':orgs,
               'all_teacher':all_teacher,
               'course_org':course_org,
               "current_page":current_page
           })

class OrgdescView(View):
       #机构首页
       def get(self, request,org_id):
           current_page="desc"
           course_org=Courseorg.objects.get(id=int(org_id))
           all_course=course_org.course_set.all()
           all_teacher=course_org.teacher_set.all()[:1]
           return render(request,"org-detail-desc.html",{
               'all_course':all_course,
               'all_teacher':all_teacher,
               'course_org':course_org,
               "current_page":current_page
           })

class OrgtteacherView(View):
       #机构首页
       def get(self, request,org_id):

           course_org=Courseorg.objects.get(id=int(org_id))
           all_course=course_org.course_set.all()[:3]
           all_teacher=course_org.teacher_set.all()
           key_word=request.GET.get('keywords',"")
           if key_word:
              all_teacher=all_teacher.filter(Q(name__icontains=key_word)|
                                             Q(work_commpy__icontains=key_word)|Q(work_position__icontains=key_word))

           return render(request,"org-detail-teachers.html",{
               'all_course':all_course,
               'all_teacher':all_teacher,
               'course_org':course_org,

           })



class AddFavView(View):
    """
    用户收藏，用户取消收藏
    """
    def post(self, request):
        fav_id = request.POST.get('fav_id', 0)
        fav_type = request.POST.get('fav_type', 0)
        user_id=request.user.id
        if not request.user.is_authenticated():
            #判断用户登录状态
            return HttpResponse('{"status":"fail", "msg":"用户未登录"}', content_type='application/json')

        exist_records = UserFavorite.objects.filter(user=request.user, fav_id=int(fav_id), fav_type=int(fav_type))
        if exist_records:
            #如果记录已经存在， 则表示用户取消收藏
            exist_records.delete()
            if int(fav_type)==1:
                course=Course.objects.get(id=int(fav_type))
                course.fav_nums-=1
                if course.fav_nums<0:
                    course.fav_nums=0
                course.save()
            elif int(fav_type)==2:
                org=Courseorg.objects.get(id=int(fav_type))
                org.fav_nums-=1
                if org.fav_nums<0:
                    org.fav_nums=0
                org.save()
            elif int(fav_type)==3:
                teacher=Teacher.objects.get(id=int(fav_type))
                teacher.fav_nums-=1
                if teacher.fav_nums<0:
                   teacher.fav_nums=0
                teacher.save()
            return HttpResponse('{"status":"success", "msg":"收藏删除成功"}', content_type='application/json')
        else:
            user_fav=UserFavorite()
            if int(fav_id)>0 and int(fav_type)>0:
                user_fav.fav_id=int(fav_id)
                user_fav.fav_type=int(fav_type)
                user_fav.user=request.user
                user_fav.save()
                if int(fav_type)==1:
                    course=Course.objects.get(id=int(fav_type))
                    course.fav_nums+=1
                    course.save()
                elif int(fav_type)==2:
                    org=Courseorg.objects.get(id=int(fav_type))
                    org.fav_nums+=1
                    org.save()
                elif int(fav_type)==3:
                    teacher=Teacher.objects.get(id=int(fav_type))
                    teacher.fav_nums+=1
                    teacher.save()
                return HttpResponse('{"status":"success", "msg":"收藏成功"}', content_type='application/json')
            else:
                 return HttpResponse('{"status":"fail", "msg":"收藏出错"}', content_type='application/json')


class teacherlistView(View):
    def get(self,request):
        all_teacher=Teacher.objects.all()
        sort_teacher=Teacher.objects.all().order_by("-work_year")[:3]
        sort = request.GET.get('sort', "")
        if sort=="hot":
            all_teacher=all_teacher.order_by("-click_nums")
        try:
             page = request.GET.get('page', 1)
        except PageNotAnInteger:
             page = 1
        p = Paginator(all_teacher,1, request=request)

        teachers = p.page(page)
        org=all_teacher.count()
        return render(request,"teachers-list.html",{
            "teacher":teachers,
            "num":org,
            "sort":sort,
            "sort_teacher":sort_teacher
        })
class teacherdetailView(View):
    def get(self,request,teacher_id):
        teacher=Teacher.objects.get(id=teacher_id)
        sort_teacher=Teacher.objects.all().order_by("-work_year")[:3]
        all_course=Course.objects.filter(teacher=teacher)
        teacher.click_nums+=1
        teacher.save()
        fav_course=False
        fav_org=False
        if  request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user,fav_id=teacher.id,fav_type=3):
                fav_course=True
            if UserFavorite.objects.filter(user=request.user,fav_id=teacher.org.id,fav_type=2):
                fav_org=True
        return render(request,"teacher-detail.html",{
            'teacher':teacher,
            "all_course":all_course,
            "sort_teacher":sort_teacher,
            "fav_org":fav_org,
            "fav_course":fav_course

        })





