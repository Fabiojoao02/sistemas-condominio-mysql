from django.urls import path
from django.views.generic.list import ListView
from . import views


urlpatterns = [
    path('', views.ListaLeitura.as_view(), name='listaleitura')
]
