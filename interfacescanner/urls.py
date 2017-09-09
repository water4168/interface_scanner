#coding:utf-8
from django.conf.urls import url
from .views import IndexView, LoginView


app_name = "interfacescanner"
urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'login/', LoginView.as_view(), name='login'),
]