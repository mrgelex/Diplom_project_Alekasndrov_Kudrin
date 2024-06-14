from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from .forms import *

class User:
    def __init__(self, userid, name, login, password, clname, clrule):
        self.userid=userid
        self.name=name
        self.login=login
        self.password=password
        self.clname=clname
        self.clrule=clrule


def showLogin(request):
    if request.method == 'POST':
        dataform=Loginform(request.POST)
        if dataform.is_valid():
            lgn=dataform.cleaned_data.get('login')
            pswd=dataform.cleaned_data.get('password')
            validUser=Usertab.objects.filter(login=lgn, password=pswd)#only(), defer()
            if validUser:
                for i in validUser:
                    userid=i.user_id
                    clientid=i.client_id
                    name=i.name
                    login=i.login
                    password=i.password
                clientData=Clienttab.objects.filter(client_id=clientid)
                for j in clientData:
                    clname=j.name
                    clrule=j.rule_id
                user=User(userid, name, login, password, clname, clrule)
            else:
                return HttpResponse('Неправильный логин или пароль!')
        else:
            return HttpResponse('Неправильный ввод!')
    form=Loginform()
    return render(request, 'authorization/login', {'form':form})

# class ClientRule:
#     def __init__(self, web, setting, control, report):
#         self.web=web
#         self.setting=setting
#         self.control=control
#         self.report=report


