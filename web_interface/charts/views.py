import plotly.express as plex
import plotly.graph_objs as plgo
import plotly.io as plio
from .forms import *
from django.shortcuts import render, redirect
from .models import *

chartAcces=20

def showCharts(request, idDev):
    def datachar(first, last, name):
        data=list(LogTimetab.objects.filter(date_local__gte=first, date_local__lte=last, device_id=idDev).values_list(name, flat=True))
        return data

    def addtrace(abscissa, ordinate, group, name, y, legend=False):
        chartWin.add_trace(plgo.Scatter(y=abscissa, x=ordinate, mode="lines", legendgroup=group, name=name, showlegend=legend), secondary_y=y)

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
    config={'displayModeBar':True, 'displaylogo': True}
    plio.templates.default = "plotly_white"
    chartWin=plex.line()
    chartWin.update_yaxes(title_text="<b>Глубина</b>, М", secondary_y=False)
    chartWin.update_yaxes(title_text="<b>Мощность</b>, %", secondary_y=True)
    chartWin.show(config=config)

    if first and last:
        datForm=TimeInterval(initial={'first':first, 'last':last})
        powerdata=datachar(first, last, 'power')
        depthdata=datachar(first, last, 'depth')
        timestamp=datachar(first, last, 'timestamp_loc')
        addtrace(powerdata, timestamp, 'Мощность', 'Мощность', False, True)
        addtrace(depthdata, timestamp, 'Глубина', 'Глубина', True, True)
        chartWin.update_layout(title="имя устройства", legend_orientation="h")
        chartWin.update_yaxes(autorange='reversed')

    else:
        datForm=TimeInterval()
    chartScript=chartWin.to_html(full_html=False)
    return render(request, 'charts/fold-list.html', {'chartScript':chartScript, 'datForm':datForm})