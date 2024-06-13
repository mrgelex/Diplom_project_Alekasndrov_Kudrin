from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from .forms import Loginform

def showLogin(request):
    if request.method == 'POST':
        logindata=Loginform(request.POST)
        if logindata.is_valid():
            pass
        else:
            return HttpResponse('Неправильный ввод данных!')