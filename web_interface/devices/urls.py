from django.urls import path
from. import views
urlpatterns = [
    path('all', views.allLists, name='all'),
    path('bushes', views.listbushes, name='bushes'),
    path('bush', views.onebash, name='bush')
]