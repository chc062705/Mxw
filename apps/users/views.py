# -*- coding:utf-8 -*-
import json
from operation.models import UserCourse,UserFavorite,UserMassage
from organization.models import Courseorg,Teacher
from course.models import Course
from django.shortcuts import render
from users.models import UserProfile,EmailVerifyRecord
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.backends import ModelBackend
from utils.minxin_until import LoginRequiredMinxin
from django.db.models import Q
from users.forms import LoginFrom,RegisterFrom,UploadImageForm,ChangepswFrom,UserinfoForm
from django.views.generic.base import View
from utils.email_send import send_register_email
from django.contrib.auth.hashers import make_password
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse,HttpResponseRedirect
# Create your views here.
class CustomBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user=UserProfile.objects.get(Q(username=username)|Q(email=username))
            if  user.check_password(password):
                return user
        except Exception as e    :
            return None

class LoginView(View):
    def get(self,request):
         return render(request,"login.html",{})
    def post(self,request):
        login_form=LoginFrom(request.POST)
        if login_form.is_valid():
            user_name=request.POST['username']
            pass_word=request.POST['password']
            user=authenticate(username=user_name,password=pass_word)
            if user:
                if user.is_active:
                    login(request,user)
                    return render(request,"index.html",{"msg":u"用户名或密码错误"})
                else:
                    return render(request,"login.html",{"msg":u"用户未激活"})
            else:
                return render(request,"login.html",{"msg":u"用户名和密码不存在","login_form":login_form})

        else:
                return render(request,"login.html",{"msg":u"请正确填写用户名和密码","login_form":login_form})
class LogoutView(View):
    def get(self,request):
        logout(request)
        from django.core.urlresolvers import reverse
        return HttpResponseRedirect(reverse("index"))

class RegisterView(View):
    def get(self,request):
        register_form=RegisterFrom()
        return render(request,"register.html",{"register_form":register_form})
    def post(self,request):
        register_form=RegisterFrom(request.POST)
        if register_form.is_valid():
            username = register_form.cleaned_data['email']
            password = register_form.cleaned_data['password']
            user_profile=UserProfile()
            user_profile.username=username
            user_profile.password=make_password(password)
            user_profile.email=username
            user_profile.is_active=False
            user_profile.save()
            usermessage=UserMassage()
            usermessage.user=user_profile
            usermessage.message=u'欢迎注册慕学在线'
            usermessage.save()
            send_register_email(username,"register")
            return render(request,"index.html",{"msg":u"用户名或密码错误","register_form":register_form})
        else:
                return render(request,"register.html",{"register_form":register_form})


class ActiveUserView(View):
    def get(self,request,active_code):
        akk=EmailVerifyRecord.objects.filter(code=active_code)
        if akk:
            for record in akk:
                email=record.email
                user=UserProfile.objects.get(email=email)
                user.is_active=True
                user.save()
        return render(request,"index.html",{})

class UserinfoView(LoginRequiredMinxin,View):
    def get(self,request):

        return render(request,"usercenter-info.html",{})
    def post(self,request):
        user_form=UserinfoForm(request.POST,instance=request.user)
        if user_form.is_valid():
            user_form.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail"}', content_type='application/json')


class UserphotoView(LoginRequiredMinxin,View):
    def post(self,request):
        image_form=UploadImageForm(request.POST,request.FILES,instance=request.user)
        if image_form.is_valid():
            image_form.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail"}', content_type='application/json')

class ChangePswView(View):

    def post(self,request):
        login_form=ChangepswFrom(request.POST)
        if login_form.is_valid():
            password1=request.POST['password1']
            password2=request.POST['password2']
            password3=request.POST['password3']
            user=request.user
            if  user.check_password(password1):
                user.password=make_password(password2)
                user.save()
                return HttpResponse('{"status":"success","msg":"修改成功"}', content_type='application/json')
            else:
                return HttpResponse('{"status":"fail","msg":"原密码错误"}', content_type='application/json')
        else:
            return HttpResponse(json.dumps(login_form.errors), content_type='application/json')

class sendemailView(View):
    def get(self,request):
        email=request.GET.get('email',"")
        if UserProfile.objects.filter(email=email):
             return HttpResponse('{"email":"邮箱已经存在"}', content_type='application/json')
        else:

           send_register_email(email,"update")
           return HttpResponse('{"status":"success"}', content_type='application/json')
class CHANGEemailView(View):
    def post(self, request):
        email = request.POST.get('email', '')
        code = request.POST.get('code', '')
        if EmailVerifyRecord.objects.filter(email=email,code=code,send_type="update"):
            user=request.user
            user.email=email
            user.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"email":"验证码出错"}', content_type='application/json')


class mycourse(LoginRequiredMinxin,View):

    def get(self,request):
        user=request.user
        all_course=UserCourse.objects.filter(user=user)
        return render(request,"usercenter-mycourse.html",{
            "all_course":all_course
        })

class favcourseView(LoginRequiredMinxin,View):
#我的收藏
    def get(self,request):
        user=request.user
        all_course=UserFavorite.objects.filter(user=user,fav_type="1")
        course_list=[]
        for fav_org in all_course:
            org_id=fav_org.fav_id
            course=Course.objects.get(id=org_id)
            course_list.append(course)

        return render(request,"usercenter-fav-course.html",{
            "all_course":course_list
        })
class favorgView(LoginRequiredMinxin,View):
#我的收藏
    def get(self,request):
        user=request.user
        all_course=UserFavorite.objects.filter(user=user,fav_type="2")
        course_list=[]
        for fav_org in all_course:
            org_id=fav_org.fav_id
            course=Courseorg.objects.get(id=org_id)
            course_list.append(course)

        return render(request,"usercenter-fav-org.html",{
            "all_course":course_list
        })
class favteaView(LoginRequiredMinxin,View):
#我的收藏
    def get(self,request):
        user=request.user
        all_course=UserFavorite.objects.filter(user=user,fav_type="3")
        course_list=[]
        for fav_org in all_course:
            org_id=fav_org.fav_id
            course=Teacher.objects.get(id=org_id)
            course_list.append(course)

        return render(request,"usercenter-fav-teacher.html",{
            "all_course":course_list
        })

class MymessageView(LoginRequiredMinxin,View):
    def get(self,request):
        user=request.user
        all_message=UserMassage.objects.filter(user=user).order_by("-add_time")
        has_read=UserMassage.objects.filter(user=request.user,has_read=False)
        for unread in has_read:
            unread.has_read=True
            unread.save()
        try:
             page = request.GET.get('page', 1)
        except PageNotAnInteger:
             page = 1
        p = Paginator(all_message,9, request=request)

        message= p.page(page)
        return render(request,"usercenter-message.html",{
            "all_message":message
        })