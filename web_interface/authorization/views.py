from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from .forms import *
import write_log as log

def showLogin(request):
    if 'user' in request.session:
        return redirect('devices')
    text=''
    if request.method == 'POST':
        dataform=Loginform(request.POST)
        if dataform.is_valid():
            lgn=dataform.cleaned_data.get('login')
            pswd=dataform.cleaned_data.get('password')
            validUser=Usertab.objects.filter(login=lgn, password=pswd)
            if validUser:
                for i in validUser:
                    userid=i.user_id
                    clientid=i.client_id
                    name=i.name
                clientData=Clienttab.objects.filter(client_id=clientid)
                for j in clientData:
                    clname=j.name
                    clrule=j.rule_id
                user={'userid':userid, 'name':name, 'clname':clname, 'clrule':clrule}
                request.session['user']=user
                print('пользователь сохранен')
                # log.write(userid, 1)
                return redirect('devices')
            else:
                text='Неправильный логин или пароль!'
        else:
            text='Неправильный ввод!'
    form=Loginform()
    return render(request, 'authorization/log-in-out.html', {'form':form, 'error':text})

def logout(request):
    session=request.session
    user=session['user']
    # log.write(user.get('userid'), 2)
    session.flush()
    return redirect('login')