# coding: utf-8
from __future__ import unicode_literals
from django.db import models
# Create your models here.


class Method(models.Model):
    name = models.CharField(max_length=10, verbose_name=u'请求方法')

    def __unicode__(self):
        return self.name


class InterFace(models.Model):
    name = models.CharField(max_length=100, verbose_name=u'接口描述')
    theurl = models.URLField(max_length=500, verbose_name=u'接口url', unique=True) #unique是否唯一
    proxy = models.GenericIPAddressField(max_length=20, verbose_name=u'代理地址', null=True, blank=True)
    postdata = models.CharField(max_length=200, verbose_name=u'post参数', blank=True) #blank是否为空
    expection = models.CharField(max_length=200, verbose_name=u'预期响应')
    created_time = models.DateTimeField(auto_now_add=True)
    method = models.ForeignKey(Method, verbose_name=u'请求方式')
    station = models.BooleanField(default=False, verbose_name="是否有效")

    class Meta:
        ordering = ["-created_time"]

    def __unicode__(self):
        return self.name    #只能返回str类型 而不能是数字


