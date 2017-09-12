# coding:utf-8
from django.views.generic.base import View
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required

from django.http import  HttpResponse,HttpResponseRedirect
from django.contrib.auth.models import User
from .forms import LoginForm
from .models import InterFace
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.


class IndexView(View):
    def get(self, request):
        interface_list = InterFace.objects.all()

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(interface_list, 2, request=request)  # 这里的数字，表示每页显示的数量

        interfaces = p.page(page)

        return render(request, 'index.html', {"interface_list": interfaces})


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
                request.session['username'] = user_name  # 将 session 信息写到服务器
                return response
            else:
                return render(request, 'login.html', {"msg":"用户名或者密码错误"})
        else:
            return render(request, 'login.html', {"msg":"请填写账号或者密码"})


@login_required  # 这个装饰器只能装饰def不能是class
def List(request):

    username = request.session.get('username', '')
    interface_list = InterFace.objects.all()
    try:
        page = request.GET.get('page', 1)
    except PageNotAnInteger:
        page = 1
    p = Paginator(interface_list, 2, request=request)  # 这里的数字，表示每页显示的数量
    interfaces = p.page(page)

    return render(request, 'list.html', {"user": username, "interface_list": interfaces})


@login_required
def Verify(request):
    interfaces_id = request.POST.get()





