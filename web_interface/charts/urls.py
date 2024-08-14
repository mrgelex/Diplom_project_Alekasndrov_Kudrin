from django.urls import path
from. import views
urlpatterns = [
    path('<int:idDev>', views.showCharts, name='showcharts'),
]