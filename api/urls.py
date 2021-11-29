from django.contrib import admin
from django.urls import path , include
from . import views


urlpatterns = [
    path('register/', views.RegisterAPI.as_view(), name='register'),
    path('resetpassword/', views.ResetPasswordAPI.as_view(), name='resetpassword'),
]