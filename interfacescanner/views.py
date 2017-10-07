# coding:utf-8

import requests, re
from django.views.generic.base import View
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from .forms import LoginForm
from .models import InterFace
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.


class IndexView(View):
    def get(self, request):
        interface_list = InterFace.objects.all()
        # 判断登录态
        if request.user.is_authenticated():
            username = request.COOKIES.get('username', '')
        else:
            username = ''

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(interface_list, 60, request=request)  # 这里的数字，表示每页显示的数量

        interfaces = p.page(page)

        return render(request, 'index.html', {"interface_list": interfaces, "username": username})


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
                response.set_cookie("username", user_name, 3600)  # 写入浏览器的cookie,失效时间3600
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
    try:
        page = request.GET.get('page', 1)
    except PageNotAnInteger:
        page = 1
    p = Paginator(interface_list, 60, request=request)  # 这里的数字，表示每页显示的数量
    interfaces = p.page(page)

    return render(request, 'list.html', {"user": username, "interface_list": interfaces})


#退出
def logout(request):
    logout(request)
    return HttpResponseRedirect(reversed("logout"))


def interfacetest(interface):

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) '
                             'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36'
               }
    #if interface.proxy:


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
                return status, resp
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
                return status, resp
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
            pass
    else:
        return HttpResponse('{"status":"fail", "msg":"用户未登录"}', content_type='application/json')


    # if not request.user.is_authenticated():
    #     # 判断用户登录状态
    #
    #
    # else:
    #     return HttpResponse('{"status":"success", "msg":"验证成功"}', content_type='application/json')










