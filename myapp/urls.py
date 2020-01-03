from django.contrib import admin
from django.urls import path
from myapp import views

urlpatterns = [
    path('', views.index, name='index'),
    path('display', views.display, name='display'),
    path('delete', views.delete, name='delete'),
    path('fetch', views.fetch, name='fetch'),
]
