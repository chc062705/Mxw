# -*- coding:utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime
from django.db import models

# Create your models here.


class City(models.Model):
    name=models.CharField(max_length=100,verbose_name="城市")
    desc=models.TextField(verbose_name=u"城市描述")
    add_time=models.DateTimeField(default=datetime.now)
    class Meta:
        verbose_name=u"城市"
        verbose_name_plural=verbose_name
    def __unicode__(self):
        return self.name


class Courseorg(models.Model):
    name=models.CharField(max_length=100,verbose_name="机构名称")
    desc=models.TextField(verbose_name=u"机构描述")
    category=models.CharField(default="pxjg",max_length=20,verbose_name=u"机构类别",choices=(('pxjg',u"培训机构"),('gr',u"个人"),('gx',u"高校")))
    click_nums=models.IntegerField(default=0,verbose_name="点击数")
    fav_nums=models.IntegerField(default=0,verbose_name="收藏人数")
    image=models.ImageField(upload_to="org/%y/%m",verbose_name="logo")
    city=models.ForeignKey(City,verbose_name="所在城市")
    type=models.CharField(max_length=5,default=u'全国知名',verbose_name="机构类型")
    students=models.IntegerField(default=0,verbose_name="学生人数")
    course_nums=models.IntegerField(default=0,verbose_name="课程数")
    adress=models.CharField(max_length=150,verbose_name="机构地址")
    add_time=models.DateTimeField(default=datetime.now)
    class Meta:
        verbose_name=u"机构名称"
        verbose_name_plural=verbose_name
    def __unicode__(self):
        return self.name
    def get_teacher_nums(self):
        return self.teacher_set.all().count()

class Teacher(models.Model):
    org=models.ForeignKey(Courseorg,verbose_name="所属机构")
    name=models.CharField(max_length=100,verbose_name="教师名称")
    points=models.TextField(verbose_name=u"教师特点")
    work_position=models.CharField(max_length=100,default="",verbose_name="公司职务")
    work_year=models.IntegerField(default=0,verbose_name='工作年限')
    work_commpy=models.CharField(max_length=50,verbose_name='就职公司')
    age=models.IntegerField(default=0,verbose_name='年龄')
    click_nums=models.IntegerField(default=0,verbose_name="点击数")
    image=models.ImageField(upload_to="teacher/%y/%m",verbose_name="教师头像",default="")
    fav_nums=models.IntegerField(default=0,verbose_name="收藏人数")
    add_time=models.DateTimeField(default=datetime.now)
    class Meta:
        verbose_name=u"教师名称"
        verbose_name_plural=verbose_name
    def __unicode__(self):
        return self.name
    def get_cur_nums(self):
        return self.course_set.all().count()
