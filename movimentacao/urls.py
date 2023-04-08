from django.urls import path
# from django.views.generic.list import ListView
from .views import ListaLeitura, ListaCalculo, RelatorioCalculosPDF, Busca

app_name = 'movimentacao'

urlpatterns = [
    path('listacalculo/', ListaCalculo.as_view(), name='listacalculo'),
    path('listaleitura/', ListaLeitura.as_view(), name='listaleitura'),
    path('relatorio_calculos_pdf/', RelatorioCalculosPDF.as_view(),
         name='relatorio_calculos_pdf'),
    path('busca/', Busca.as_view(), name='busca')

]
