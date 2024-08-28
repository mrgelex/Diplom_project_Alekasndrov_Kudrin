from django.shortcuts import render, redirect
from .forms import *
from devices.models import Devicetab
import write_log as log
import socket_mod as s
import math as m
import perm_for_web as p

viewSetpAcc=p.viewSP
changSetAcc=p.changSP

def showSetpoints(request, idDev):
    def correct(data):
        dictdata=data.cleaned_data
        for i in dictdata:
            if i != 'EnUpECN':
                if not dictdata.get(i):
                    dictdata[i]=setpoint.get(i)
            if i in ['WorkSpeed', 'ManualSpeed', 'CollarSpeed']:
                dictdata[i]=m.trunc(dictdata.get(i)*10)
        return dictdata
    rel=False
    if not 'user' in request.session:
        return redirect('login')
    if not 'accesD' in request.session:
        return redirect('devices')
    accesD=request.session['accesD']
    user=request.session['user']
    mess=''
    if not str(idDev) in accesD:
        return render(request, 'devices/warning.html', {'text':'Извините, у Вас нет доступа к такому ресурсу<br/>Пожалуйста, используйте графический интерфейс для доступа к Вашим ресурсам', 'user':user})
    accesLvl=accesD.get(str(idDev))
    devData=list(Devicetab.objects.filter(device_id=idDev).values('name_user', 'description'))
    devData=dict(devData[0])
    print(devData)
    if accesLvl < viewSetpAcc:
        return render(request, 'devices/warning.html', {'text':'Извините, Ваш уровень доступа ограничен', 'user':user})
    setpoint=s.operData(idDev, False)
    if not setpoint:
        mess='Нет связи!'
    setP=Setpoints()
    if accesLvl < changSetAcc:
        if request.method=='POST':
            mess='Вы не можете изменять уставки!'
        but=False
        setP.initial=setpoint
        setP.disable()
    else:
        err=False
        but=True
        if request.method=='POST':
            data=Setpoints(request.POST)
            if data.is_valid():
                if 'SPque' in request.session:
                    SPque=request.session['SPque']
                else:
                    SPque={}
                if not SPque.get(str(idDev)):
                    dictdata=correct(data)
                    del dictdata['Username1'] #удаление имени
                    del dictdata['Username2'] #удаление имени
                    err, mess=s.writeSP(idDev, dictdata)
                    
                    if not err:
                        SPd={}
                        SPd[str(idDev)]=dictdata #вида {id:{a:1, b:2...n:n}}
                        SPque.update(SPd)
                        request.session['SPque']=SPque
                        # log.write(user.get('userid'), 1, idDev)

            else:
                mess='Неправильная форма ввода уставок!'
        if 'SPque' in request.session:
            SPque=request.session['SPque']
            if SPque:
                sp=SPque.get(str(idDev))
                if sp:
                    print('sp from session', sp)
                    sp['EnUpECN']=bool(sp.get('EnUpECN'))
                    setpoint=sp
                    setP.disable()
                    rel=True
                    but=False
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
        return render(request, 'setpoints/setpoints-rel.html', {'setP': setP, 'user':user, 'but':but, 'mess':mess, 'devData':devData})
    else:
        return render(request, 'setpoints/setpoints.html', {'setP': setP, 'user':user, 'but':but, 'mess':mess, 'devData':devData})
    
        