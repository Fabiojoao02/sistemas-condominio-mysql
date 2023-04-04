from django.urls import path
# from django.views.generic.list import ListView
from .views import ListaLeitura, ListaCalculo, RelatorioCalculosPDF

app_name = 'movimentacao'

urlpatterns = [
    path('', ListaCalculo.as_view(), name='listacalculo'),
    path('listaleitura/', ListaLeitura.as_view(), name='listaleitura'),
    path('relatoriocalculospdf/', RelatorioCalculosPDF.as_view(),
         name='relatoriocalculospdf'),

]
