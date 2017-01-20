# -*- coding:utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime
from django.db import models

from django.contrib.auth.models import AbstractUser
# Create your models here.
class UserProfile(AbstractUser):
    nick_name=models.CharField(max_length=50,verbose_name=u'昵称')
    birday=models.DateField(null=True,blank=True,verbose_name=u'生日')
    gender=models.CharField(choices=(('male',u'男'),('fumale',u'女'),('baomi',u'保密')),default='baomi',max_length=100,verbose_name=u'性别')
    adress=models.CharField(null=True,blank=True,max_length=150,verbose_name=u'地址')
    mobile=models.CharField(null=True,blank=True,max_length=11,verbose_name=u'手机')
    image=models.ImageField(upload_to="image/%y/m",default="")
    class Meta:
        verbose_name=u'用户信息'
        verbose_name_plural=verbose_name

    def __unicode__(self):
        return self.username
    def get_usernnread(self):
        from operation.models import UserMassage
        return UserMassage.objects.filter(user=self,has_read=False).count()

class EmailVerifyRecord(models.Model):
    code=models.CharField(max_length=20,verbose_name=u'验证码')
    email=models.EmailField(max_length=50,verbose_name=u"邮箱")
    send_type=models.CharField(max_length=50,choices=(("register",u"注册"),("forget",u"忘记密码"),("update",u"更新邮箱")))
    send_time=models.DateTimeField(default=datetime.now)
    class Meta:
        verbose_name=u'邮箱验证码'
        verbose_name_plural=verbose_name

class Banner(models.Model):
    tittle=models.CharField(max_length=100,verbose_name=u"标题")
    image=models.ImageField(upload_to="banner/%y/%m",verbose_name=u"轮播图")
    url=models.URLField(max_length=200,verbose_name=u"访问地址")
    index=models.IntegerField(default=100,verbose_name=u"顺序")
    add_time=models.DateTimeField(default=datetime.now,verbose_name=u"添加时间")
    class Meta:
        verbose_name=u'轮播图'
        verbose_name_plural=verbose_name