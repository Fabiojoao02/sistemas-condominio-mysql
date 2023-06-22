from django.urls import path
# from django.views.generic.list import ListView
from .views import ListaLeitura, ListaCalculo, RelatorioCalculosPDF, Busca
from . import views
# from django.urls import reverse
# from django.shortcuts import redirect

app_name = 'movimentacao'

urlpatterns = [
    path('listacalculo/', ListaCalculo.as_view(), name='listacalculo'),
    path('listaleitura/', ListaLeitura.as_view(), name='listaleitura'),
    path('relatorio_calculos_pdf/', RelatorioCalculosPDF.as_view(),
         name='relatorio_calculos_pdf'),
    path('busca/', Busca.as_view(), name='busca'),
    # path('create/', views.expense_create, name='expense_create'),
    path('create/<int:idb>/<str:ma>', views.expense_create, name='expense_create'),
    path('<int:pk>/', views.expense_detail, name='expense_detail'),
    path('<int:pk>/update', views.expense_update, name='expense_update'),
    path('<int:pk>/delete', views.expense_delete, name='expense_delete'),
    path('movimentacao/paid/', views.expense_paid, name='expense_paid'),
    path('movimentacao/no-paid/', views.expense_no_paid, name='expense_no_paid'),
]


# def get_reverse(request):
#    url = reverse('create-contact')
#    return redirect(url)
