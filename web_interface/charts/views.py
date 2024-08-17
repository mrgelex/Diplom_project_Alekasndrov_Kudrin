import plotly.express as plex
import plotly.graph_objs as plgo
import plotly.io as plio
from .forms import *
from django.shortcuts import render, redirect
from .models import *
import perm_for_web as p

chartAcces=p.shart
timeout=5

def showCharts(request, idDev):
    def datachar(first, last, name):
        data=list(LogTimetab.objects.filter(timestamp_loc__gte=first, timestamp_loc__lte=last, device_id=idDev).values_list(name, flat=True))
        return data

    def addtrace(abscissa, ordinate, group, name, legend, color, y=None):
        chartWin.add_trace(plgo.Scatter(y=abscissa, x=ordinate, mode='lines', legendgroup=group, name=name, showlegend=legend, yaxis=y, marker=dict(color=color)))

    if not 'user' in request.session:
        return redirect('login')
    user=request.session['user']
    if not 'accesD' in request.session:
        return redirect('devices')
    accesD=request.session['accesD']
    if not str(idDev) in accesD:
        return render(request, 'devices/warning.html', {'text':'Извините, у Вас нет доступа к такому ресурсу'})
    if accesD.get(str(idDev)) < chartAcces:
        return render(request, 'devices/warning.html', {'text':'Извините, Ваш уровень доступа ограничен'})


    first=request.GET.get('first')
    last=request.GET.get('last')
    # config={'displayModeBar':True, 'displaylogo': False}
    plio.templates.default = 'plotly_white'
    chartWin=plex.line()
    # chartWin.show(config={'displayModeBar':True, 'displaylogo': False})

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
            addtrace(i[2], i[0], 'Глубина', 'Глубина',  swichShowLeg, 'blue', 'y2')
            swichShowLeg=False

        chartWin.update_layout(title='имя устройства', legend_orientation='h', yaxis=dict(title='Глубина, М'), yaxis2=dict(title='Мощность, %', overlaying='y', side='right'))
        chartWin.update_yaxes(autorange='reversed')
    else:
        datForm=TimeInterval()
    chartScript=chartWin.to_html(full_html=False)
    return render(request, 'charts/charts.html', {'chartScript':chartScript, 'datForm':datForm})


