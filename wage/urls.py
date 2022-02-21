from django.urls import path

from . import views

urlpatterns = [
    path('', views.getdatafrominter, name='getdatafrominter'),
]
