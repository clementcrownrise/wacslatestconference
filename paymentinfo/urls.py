from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [

    path('', views.paymentinfo, name='paymentinfo'),
    #path(', views.create, name='create')
 
]