from django.urls import path
from django.views.generic.list import ListView
from . import views

app_name = 'movimentacao'

urlpatterns = [
    # path('', views.ListaLeitura.as_view(), name='listaleitura')
    path('', views.listaleitura, name='listaleitura')
]
