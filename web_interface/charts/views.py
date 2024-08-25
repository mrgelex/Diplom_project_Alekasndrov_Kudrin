import plotly.express as plex
import plotly.graph_objs as plgo
import plotly.io as plio
from .forms import *
from django.shortcuts import render, redirect
from .models import *
from devices.models import Devicetab
import perm_for_web as p

chartAcces=p.shart
timeout=5

def showCharts(request, idDev):
    def datachar(first, last, name):
        data=list(LogTimetab.objects.filter(timestamp_loc__gte=first, timestamp_loc__lte=last, device_id=idDev).values_list(name, flat=True))
        return data

    def addtrace(abscissa, ordinate, group, name, legend, color, y=None):
        chartWin.add_trace(plgo.Scatter(y=abscissa, x=ordinate, mode='lines', legendgroup=group, name=name, showlegend=legend, yaxis=y, marker=dict(color=color), textfont_size=20))

    if not 'user' in request.session:
        return redirect('login')
    user=request.session['user']
    if not 'accesD' in request.session:
        return redirect('devices')
    accesD=request.session['accesD']
    if not str(idDev) in accesD:
        return render(request, 'devices/warning.html', {'text':'Извините, у Вас нет доступа к такому ресурсу<br/>Пожалуйста, используйте графический интерфейс для доступа к Вашим ресурсам', 'user':user})
    if accesD.get(str(idDev)) < chartAcces:
        return render(request, 'devices/warning.html', {'text':'Извините, Ваш уровень доступа ограничен', 'user':user})


    first=request.GET.get('first')
    last=request.GET.get('last')
    plio.templates.default = 'plotly_white'
    chartWin=plex.line(height=750)
    if first and last:
        datForm=TimeInterval(initial={'first':first, 'last':last})
        powerdata=datachar(first, last, 'power')
        depthdata=datachar(first, last, 'depth')
        timestamp=datachar(first, last, 'timestamp_loc')
        listSet=[]
        cp=0
        lastind=len(timestamp)-1
        for j in timestamp:
            actind=timestamp.index(j)
            if actind != lastind:
                nextind=actind+1
                nextit=timestamp[nextind]
                diff=nextit - j
                if diff.total_seconds() > timeout*60:
                    listSet.append((timestamp[cp:nextind], powerdata[cp:nextind], depthdata[cp:nextind]))
                    cp=nextind
            else:
                listSet.append((timestamp[cp:], powerdata[cp:], depthdata[cp:]))
        swichShowLeg=True
        for i in listSet:
            addtrace(i[1], i[0], 'Мощность', 'Мощность',  swichShowLeg, 'red')
            addtrace(i[2], i[0], 'Глубина', 'Глубина',  swichShowLeg, 'orange', 'y2')
            swichShowLeg=False
        device=Devicetab.objects.get(device_id=idDev)
        chartWin.update_layout(title=device.description, yaxis=dict(title='Глубина, М'), yaxis2=dict(title='Мощность, %', overlaying='y', side='right') ,title_font_size=20, legend_font_size=15)
        chartWin.update_yaxes(autorange='reversed')
    else:
        datForm=TimeInterval()
    chartScript=chartWin.to_html(full_html=False)
    return render(request, 'charts/charts.html', {'chartScript':chartScript, 'datForm':datForm, 'user':user})


