from django.urls import path
from. import views
urlpatterns = [
    path('', views.allFold, name='devices'),
    path('<int:idFol>', views.showBush, name='showbush')
]