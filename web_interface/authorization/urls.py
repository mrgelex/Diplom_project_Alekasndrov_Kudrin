from django.urls import path
from. import views
urlpatterns = [
    path('login', views.showLogin, name='login'),
    path('logout', views.logout, name='logout'),
]