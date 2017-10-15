# coding:utf-8
from django import forms
from .models import InterFace


class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, min_length=3)


class InterfaceForm(forms.ModelForm):
    class Meta:
        model = InterFace
        fields = ['name', 'theurl', 'proxy', 'postdata', 'expection', 'method']





