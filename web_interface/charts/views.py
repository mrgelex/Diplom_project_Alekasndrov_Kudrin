import plotly.express as plex
import plotly.graph_objs as plg
from .forms import *
from django.shortcuts import render

def showCharts(request, idDev):
    first=request.GET.get('first')
    last=request.GET.get('last')
    chartWin=plex.line()
    if first and last:
        datForm=TimeInterval(initial={'first':first, 'last':last})

    else:
        datForm=TimeInterval()
    chartScript=chartWin.to_html(full_html=False)
    return render(request, 'charts/fold-list.html', {'chartScript':chartScript, 'datForm':datForm})