from django.contrib import admin
from django.urls import path
from . import views 
from .views import create_super_admin

urlpatterns = [
    path('', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('myconferences/', views.myconferences, name='myconferences'),
    path('myconferencedetails/<int:id>/', views.myconferencedetails, name='myconferencedetails'),
    

    path('resetPassword_validate/<uidb64>/<token>/', views.resetPassword_validate,
          name='resetPassword_validate'),
    path('forgot-password/', views.forgotPassword, name='forgotPassword'),
    path('resetPassword/', views.resetPassword, name='resetPassword'),
]