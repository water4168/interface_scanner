# coding:utf-8

import requests, re
from django.views.generic.base import View
from django.shortcuts import render, get_object_or_404
from django.contrib import auth
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from .forms import LoginForm, InterfaceForm
from .models import InterFace, Method
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger


# 首页
class IndexView(View):
    def get(self, request):
        interface_list = InterFace.objects.all()
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(interface_list, 60, request=request)  # 这里的数字，表示每页显示的数量

        interfaces = p.page(page)

        return render(request, 'index.html', {"interface_list": interfaces})


# 实现登录
class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_name = request.POST.get("username", "")
            pass_word = request.POST.get("password", "")

            user = authenticate(username=user_name, password=pass_word)
            if user is not None:
                login(request, user)
                response = HttpResponseRedirect('/list/')  # 登录成功跳转list
                response.set_cookie("username", user_name, 60)  # 写入浏览器的cookie,失效时间3600
                request.session['username'] = user_name  # 将 session 信息写到服务器
                return response
            else:
                return render(request, 'login.html', {"msg":"用户名或者密码错误"})
        else:
            return render(request, 'login.html', {"msg":"请填写账号或者密码"})


@login_required  # 这个装饰器只能装饰def不能是class
def List(request):

    username = request.COOKIES.get('username', '')
    interface_list = InterFace.objects.all()

    # ====================搜索==================================
    search_keywords = request.GET.get('keywords', "")
    if search_keywords:
        interface_list = interface_list.filter(
            Q(name__icontains=search_keywords) |
            Q(theurl__icontains=search_keywords)
        )

    # =====================分页==================================
    try:
        page = request.GET.get('page', 1)
    except PageNotAnInteger:
        page = 1
    p = Paginator(interface_list, 60, request=request)  # 这里的数字，表示每页显示的数量
    interfaces = p.page(page)

    return render(request, 'list.html', {"user": username, "interface_list": interfaces})


# 退出
def logouted(request):
    auth.logout(request)
    return HttpResponseRedirect("/login/")
    # response = HttpResponseRedirect('/login/')
    # response.delete_cookie('username')
    # return response


# 接口验证方法，给下面的验证接口调用
def interfacetest(interface):

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) '
                             'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36'
               }

    if interface.method.name == "get":
        r = requests.get(url=interface.theurl, headers=headers
                         )
        status = r.status_code
        resp = r.text

        if status == 200:
            if re.search(interface.expection, resp):
                interface.station = True
                interface.save()
                print ('found it')
                #return status, resp
            else:
                print ('no found ')

        else:
            print status

    elif interface.method.name == "post":
        interface.postdata = eval(interface.postdata )
        r = requests.post(url=interface.theurl, data=interface.postdata, headers=headers
                          )
        status = r.status_code
        resp = r.text

        if status == 200:
            if re.search(interface.expection, resp):
                interface.station = True
                interface.save()
                print ('found it')
                #return status, resp
            else:
                print ('no found ')

        else:
            print status

    else:
        print('method get wrong!')


@login_required
def Verify(request):
    '''验证ajax传过来的接口id'''
    if request.user.is_authenticated():
        interfaces_id = request.POST.getlist("Idlist[]")  # getlist("xxx[]") 这样才能取到前端传古来的list
        if len(interfaces_id):
            for id in interfaces_id:
                interface = InterFace.objects.get(id=int(id))  # 注意要str-->int
                interfacetest(interface)

            return HttpResponse('{"status":"success", "msg":"已验证完毕"}', content_type='application/json')

        else:
            return HttpResponse('{"status":"fail", "msg":"请勾选接口"}', content_type='application/json')
    else:
        return HttpResponse('{"status":"fail", "msg":"用户未登录"}', content_type='application/json')


# 新增接口
@login_required
def createone(request):
    if request.method == "GET":
        form = InterfaceForm()
        return render(request, 'new_interface.html', {"interface_form": form})

    if request.method == "POST":

        form = InterfaceForm(request.POST)

        if form.is_valid():
            interface_dec = request.POST.get("name", "")
            interface_url = request.POST.get("theurl", "")
            if InterFace.objects.filter(theurl=interface_url):
                return render(request, "new_interface.html", {"interface_form": form, "msg": "url已存在"})
            interface_meth = request.POST.get("method", "")
            interface_pro = request.POST.get("proxy", "")
            interface_data = request.POST.get("postdata", "")
            interface_exp = request.POST.get("expection", "")

            newInterface = InterFace()

            newInterface.name = interface_dec
            newInterface.theurl = interface_url
            if interface_meth =='1':
                method = Method.objects.get(pk=1)
                newInterface.method = method
            else:
                method = Method.objects.get(pk=2)
                newInterface.method = method

            newInterface.proxy = interface_pro
            newInterface.postdata = interface_data
            newInterface.expection = interface_exp
            newInterface.station = False
            newInterface.save()

            response = HttpResponseRedirect('/list/')
            return response

        else:
            return render(request, "new_interface.html", {"interface_form": form, "msg": "表单错误"})


# 重置所有的接口状态
@login_required
def RemoveStation(request):
    if request.method == 'GET':
        InterFaces = InterFace.objects.all()
        for one in InterFaces:
            one.station = False
            one.save()

        response = HttpResponseRedirect('/list/')
        return response
    else:
        pass


# 删除选中的接口
@login_required
def Delete(request):
    '''验证ajax传过来的接口id'''
    if request.user.is_authenticated():
        interfaces_id = request.POST.getlist("Idlist[]")  # getlist("xxx[]") 这样才能取到前端传古来的list
        if len(interfaces_id):
            for id in interfaces_id:
                interface = InterFace.objects.get(id=int(id))  # 注意要str-->int
                interface.delete()
                return HttpResponse('{"status":"success", "msg":"删除成功"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail", "msg":"删除失败"}', content_type='application/json')
    else:
        return HttpResponse('{"status":"fail", "msg":"用户没有权限"}', content_type='application/json')















