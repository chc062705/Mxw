# -*- coding:utf-8 -*-
from __future__ import unicode_literals
from organization.models import Courseorg,Teacher
from django.db import models
from datetime import datetime
# Create your models here.


class Course(models.Model):
    course_org=models.ForeignKey(Courseorg,verbose_name=u"机构",null=True,blank=True)
    name=models.CharField(max_length=50,verbose_name=u'课程名称')
    need_know=models.CharField(max_length=350,default="",verbose_name=u'课程须知')
    teacher_tell=models.CharField(max_length=350,default="",verbose_name=u'老师告诉')
    desc=models.CharField(max_length=300,verbose_name=u'课程简介')
    tag=models.CharField(max_length=300,default="",verbose_name=u'课程标签')
    detail=models.TextField(verbose_name=u'课程详情')
    is_banner=models.BooleanField(default=False,verbose_name=u'是否广告位置')
    teacher=models.ForeignKey(Teacher,verbose_name=u"教师",null=True,blank=True)
    degree=models.CharField(choices=(('cj',u'初级'),('zj',u'中级'),('gj',u'高级')),max_length=2,verbose_name=u'难度')
    leare_time=models.IntegerField(default=0,verbose_name=u'学习时长')
    students=models.IntegerField(default=0,verbose_name=u'学习人数')
    fav_nums=models.IntegerField(default=0,verbose_name=u'收藏人数')
    image=models.ImageField(upload_to="course/%y/m",max_length=100,verbose_name=u"封面图片")
    click_nums=models.IntegerField(default=0,verbose_name=u'点击数')
    category=models.CharField(default="后端开发",max_length=300,verbose_name=u'课程类别')
    add_time=models.DateTimeField(default=datetime.now,verbose_name=u'添加时间')

    class Meta:
        verbose_name=u"课程"
        verbose_name_plural=verbose_name
    def __unicode__(self):
        return self.name
    def get_zj_nums(self):
        all_lesoon=self.lesson_set.all().count()
        return all_lesoon
    def get_learn_user(self):
        return self.usercourse_set.all()[:5]
    def get_zjxx_nums(self):
        all_lesoon=self.lesson_set.all()
        return all_lesoon

class Lesson(models.Model):
    course=models.ForeignKey(Course,verbose_name=u"课程")
    name=models.CharField(max_length=100,verbose_name=u"章节名称")

    add_time=models.DateTimeField(default=datetime.now,verbose_name=u'添加时间')
    class Meta:
        verbose_name=u"章节"
        verbose_name_plural=verbose_name
    def __unicode__(self):
        return self.name
    def get_video(self):
        all_lesoon=self.video_set.all()
        return all_lesoon

class Video(models.Model):
    name=models.CharField(max_length=100,verbose_name=u"视频名称")
    lesson=models.ForeignKey(Lesson,verbose_name=u"章节")
    video_time=models.IntegerField(default=0,verbose_name=u'视频时长')
    url=models.CharField(max_length=200,default="",verbose_name=u"访问地址")
    add_time=models.DateTimeField(default=datetime.now,verbose_name=u'添加时间')
    class Meta:
        verbose_name=u"视频"
        verbose_name_plural=verbose_name
    def __unicode__(self):
        return self.name


class CourseResource(models.Model):
    course=models.ForeignKey(Course,verbose_name=u"课程")
    name=models.CharField(max_length=100,verbose_name=u"章节名称")
    download=models.FileField(upload_to="course/resource/%y/m",verbose_name="上传文件")
    add_time=models.DateTimeField(default=datetime.now,verbose_name=u'添加时间')
    class Meta:
        verbose_name=u"课程资源"
        verbose_name_plural=verbose_name
    def __unicode__(self):
        return self.name