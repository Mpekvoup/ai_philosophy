"""
URL configuration for ai_philosopher project.
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('ai_philosopher.philosopher.urls')),
]
