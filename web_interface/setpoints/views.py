from django.shortcuts import render, redirect
from .forms import *
from devices.models import Devicetab
import write_log as log
import socket_mod as s
import math as m

viewSetpAcc=30
changSetAcc=40

def showSetpoints(request, idDev):
    rel=False
    if not 'user' in request.session:
        return redirect('login')
    if not 'accesD' in request.session:
        return redirect('devices')
    accesD=request.session['accesD']
    mess=''
    if not str(idDev) in accesD:
        return render(request, 'devices/warning.html', {'text':'Извините, у Вас нет доступа к такому ресурсу'})
    accesLvl=accesD.get(str(idDev))
    devData=dict(Devicetab.objects.filter(device_id=idDev).values('name_user', 'description'))
    if accesLvl < viewSetpAcc:
        return render(request, 'devices/warning.html', {'text':'Извините, Ваш уровень доступа ограничен'})
    user=request.session['user']
    setpoint=s.operData(idDev, False)
    if not setpoint:
        mess='Нет связи'
    SPd={}
    setP=Setpoints()
    if accesLvl < changSetAcc:
        if request.method=='POST':
            mess='Вы не можете изменять уставки!'
        but=False
        setP.initial=setpoint
        setP.disable()
    else:
        but=True
        if request.method=='POST':
            data=Setpoints(request.POST)
            if data.is_valid():
                dictdata=data.cleaned_data
                for i in dictdata:
                    if i != 'EnUpECN':
                        if not dictdata.get(i):
                            dictdata[i]=setpoint.get(i)
                    if i in ['WorkSpeed', 'ManualSpeed', 'CollarSpeed']:
                        dictdata[i]=m.trunc(dictdata.get(i)*10)
                setpoint=dictdata
                print('для инициализации', dictdata)
                print('для записи', dictdata)
                err, mess=s.writeSP(idDev, setpoint)
                if not err:
                    SPd[str(idDev)]=setpoint #вида {id:{a:1, b:2...n:n}}
                    if 'SPque' in request.session:
                        SPque=request.session['SPque']
                        if SPque.get(str(idDev)):
                            mess='Сейчас уставки менять нельзя, дождитесь окончания записи'
                        SPque.update(SPd)
                    else:
                        SPque=SPd
                    request.session['SPque']=SPque
                    # log.write(user.get('userid'), 1, idDev)
                    print('лог типа записался')
            else:
                mess='Неправильная форма ввода уставок!'

        if 'SPque' in request.session:
            SPque=request.session['SPque']
            if SPque:
                sp=SPque.get(str(idDev))
                if sp:
                    print('sp from session', sp)
                    setpoint=sp
                    setP.disable()
                    rel=True
                    but=False
                    if not request.method=='POST':
                        res, rmess=s.result(idDev)
                        if res:
                            del SPque[str(idDev)]
                            request.session['SPque']=SPque
                            but=True
                            rel=False
                            setpoint=s.operData(idDev, False)
                            setP=Setpoints()
                        mess=rmess
        setP.initial=setpoint
    if rel:
        return render(request, 'setpoints/setpoints-rel.html', {'setP': setP, 'user':user, 'but':but, 'mess':mess})
    else:
        return render(request, 'setpoints/setpoints.html', {'setP': setP, 'user':user, 'but':but, 'mess':mess})
    
        