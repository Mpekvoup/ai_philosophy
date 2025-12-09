"""
URL конфигурация для приложения philosopher.
"""
from django.urls import path
from . import views

app_name = 'philosopher'

urlpatterns = [
    path('', views.index, name='index'),
    path('api/ask/', views.ask_philosopher, name='ask_philosopher'),
]
