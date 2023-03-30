from django.urls import path
# from django.views.generic.list import ListView
from .views import ListaLeitura

app_name = 'movimentacao'

urlpatterns = [
    # path('', views.ListaLeitura.as_view(), name='listaleitura')
    path('', ListaLeitura.as_view(), name='listaleitura')
]
