from django.urls import path
from rango import views

urlpatterns = [
    path('index', views.index, name='index'),
]
