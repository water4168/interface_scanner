# coding:utf-8
from django.views.generic.base import View
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from .forms import LoginForm
from .models import InterFace
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.


class IndexView(View):
    def get(self, request):
        return render(request, 'login.html')


class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        interface_list = InterFace.objects.all()

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(interface_list, 1, request=request)  #注意这里一个数字5，表示每页显示的数量

        interfaces = p.page(page)

        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_name = request.POST.get("username", "")
            pass_word = request.POST.get("password", "")

            user = authenticate(username=user_name, password=pass_word)
            if user is not None:
                login(request, user)
                return render(request, 'list2.html', {"interface_list": interfaces})
            else:
                return render(request, 'login.html', {"msg":"用户名或者密码错误"})
        else:
            return render(request, 'login.html', {"msg":"请填写账号或者密码"})







