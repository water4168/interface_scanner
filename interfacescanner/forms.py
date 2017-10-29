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

# class InterfaceForm(forms.Form):
#     interfacename = forms.CharField(required=True, max_length=100)
#     theurl = forms.CharField(required=True)
#     method = forms.CharField(required=True)
#     proxy = forms.CharField(required=False)
#     postdata = forms.CharField(required=False)
#     expection = forms.CharField(required=True)




