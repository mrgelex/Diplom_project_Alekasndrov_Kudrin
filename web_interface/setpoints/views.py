from django.shortcuts import render, redirect
from .forms import *
from devices.models import Devicetab
import write_log as log
import socket_mod as s

viewSetpAcc=30
changSetAcc=40

def showSetpoints(request, idDev):
    if not 'user' in request.session:
        return redirect('login')
    if not 'accesD' in request.session:
        return redirect('devices')
    accesD=request.session['accesD']
    mess=''
    if not idDev in accesD:
        return render(request, 'devices/warning.html', {'text':'Извините, у Вас нет доступа к такому ресурсу'})
    accesLvl=accesD.get(idDev)
    devData=dict(Devicetab.objects.filter(device_id=idDev).values('name_user', 'description'))
    if accesLvl < viewSetpAcc:
        return render(request, 'devices/warning.html', {'text':'Извините, Ваш уровень доступа ограничен'})
    user=request.session['user']
    setpoint={}
    setP=Setpoints()
    if accesLvl < changSetAcc:
        if request.method=='POST':
            mess=''
        setP.initial=setpoint
        Setpoints.disable(setP)
    else:
        if request.method=='POST':
            data=Setpoints(request.POST)
            if data.is_valid():
                dictdata=data.cleaned_data
                for i in dictdata:
                    if not dictdata.get(i):
                        dictdata[i]=setpoint.get(i)
                setpoint=dictdata
                mess=''
                log.write(user.get('userid'), 1, idDev)
            else:
                mess=''
        setP.initial=setpoint
