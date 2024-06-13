from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from .forms import *

def showLogin(request):
    if request.method == 'POST':
        dataform=Loginform(request.POST)
        if dataform.is_valid():
            lgn=dataform.cleaned_data.get('login')
            pswd=dataform.cleaned_data.get('password')
            validUser=Usertab.objects.filter(login=lgn, password=pswd)
            if validUser:
                pass
            else:
                return HttpResponse('Неправильный логин или пароль!')
        else:
            return HttpResponse('Неправильный ввод!')
    form=Loginform()
    return render(request, 'authorization/login', {'form':form})