#coding:utf-8
from django.contrib import admin
from .models import InterFace, Method

# Register your models here.
class InterFaceAdmin(admin.ModelAdmin):
    list_display = ["name",
                    "theurl",
                    "proxy",
                    "postdata",
                    "expection",
                    "created_time",
                    "method",
                    "station"]


admin.site.register(InterFace, InterFaceAdmin)
admin.site.register(Method)
