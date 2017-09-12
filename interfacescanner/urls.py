#coding:utf-8
from django.conf.urls import url
from .views import IndexView, LoginView
from .import views


app_name = "interfacescanner"
urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'login/$', LoginView.as_view(), name='login'),
    url(r'list/$', views.List, name='list'),
    url(r'list/verify/$', views.Verify, name='verify'),

]