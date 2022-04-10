from django.urls import path

from . import views

urlpatterns = [
    path('', views.getdatafrominter, name='getdatafrominter'),
    path('leavedata', views.leavedata, name='leavedata'),
    path('searchwage', views.searchwage, name='searchwage'),
]
