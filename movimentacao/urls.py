from django.urls import path
# from django.views.generic.list import ListView
from .views import ListaLeitura, ListaCalculo, RelatorioCalculos

app_name = 'movimentacao'

urlpatterns = [
    path('', ListaCalculo.as_view(), name='listacalculo'),
    path('listaleitura/', ListaLeitura.as_view(), name='listaleitura'),
    path('relatoriocalculos/', RelatorioCalculos.as_view(),
         name='relatoriocalculos'),

]
