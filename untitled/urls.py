# -*- coding:utf-8 -*-
"""untitled URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url,include
from django.views.generic import TemplateView
from apps.organization.views import OrgView
#使用media处理图片是配置
from django.views.static import serve
from untitled.settings import MEDIA_ROOT,STATIC_ROOT
from apps.users.views import LoginView,RegisterView,ActiveUserView,LogoutView,IndexView,page_404
import xadmin
urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),
    url('^$',IndexView.as_view(),name="index"),
    url('^login/$',LoginView.as_view(),name="login"),
    url('^logout/$',LogoutView.as_view(),name="logout"),
    url('^register/$',RegisterView.as_view(),name="register"),
    url(r'^captcha/', include('captcha.urls')),
    url('^active/(?P<active_code>.*)/$',ActiveUserView.as_view(),name="active"),


    #课程机构url配置
    url(r'^org/', include('organization.urls',namespace="org")),
    url(r'^course/', include('course.urls',namespace="course")),
    url(r'^user/', include('users.urls',namespace="user")),

    #配置上传文件访问media
    url(r"^media/(?P<path>.*)$",serve,{'document_root':MEDIA_ROOT}),
    url(r"^static/(?P<path>.*)$",serve,{'document_root':STATIC_ROOT})

    #ieetffmmacbycbux；rxbsrtcrjjxbctc
]
handler404='users.views.page_404'
handler500='users.views.page_500'