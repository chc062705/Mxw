# -*- coding:utf-8 -*-
from django.conf.urls import url,include
from users.views import UserinfoView,UserphotoView,ChangePswView,sendemailView,CHANGEemailView,mycourse,favcourseView,favorgView,favteaView,MymessageView
urlpatterns = [
     url(r'^info/$',UserinfoView.as_view(),name="user_info"),
    #更改头像
    url(r'^image/upload/$',UserphotoView.as_view(),name="image_upload"),
    #用户中心密码修改
    url(r'^update/psw/$',ChangePswView.as_view(),name="User_change"),
    #修改邮箱获取验证码
    url(r'^send/email/$',sendemailView.as_view(),name="email_send"),
    url(r'^change/email/$',CHANGEemailView.as_view(),name="CHANGE_send"),
    #我的课程
    url(r'^mycourse/$',mycourse.as_view(),name="user_mycourse"),
    #我的收藏课程
    url(r'^myfavcourse/$',favcourseView.as_view(),name="user_myfavcourse"),
    url(r'^myfavorg/$',favorgView.as_view(),name="user_myfavorg"),
    url(r'^myfavtea/$',favteaView.as_view(),name="user_myfavtea"),
    url(r'^mymessage/$',MymessageView.as_view(),name="user_mymessage"),
]