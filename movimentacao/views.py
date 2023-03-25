# from django.views.generic.list import ListView
# from django.views.generic.detail import DetailView
from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from django.contrib import messages
# from django.views import View
# from . import models
from . models import Leituras
# from django.db import connection
from django.db.models import Count


# class ListaLeitura(ListView):
# def get(self, *args, **kwargs):
#     messages.error(self.request, 'Erro de teste...')
#     return redirect(self.request.META[HTTP_REFERER])
# def your_view(request):
# query_ = "select  id_morador, mesano from leituras where mesano = '022023'"
def listaleitura(request):
    model = Leituras.objects.all()
    model = Leituras.objects.aggregate(total=Count('id_leituras'),)
    contexto = {
        'leituras': model
    }

    print(model.query)
    return render(request, 'movimentacao/lista_leitura.html', contexto)
#    template_name = 'movimentacao/lista_leitura.html'
 #   context_object_name = 'leituras'
    paginate_by = 15

    # with connection.cursor() as cursor:
    # cursor.execute(query)

    # leituras = cursor.fetchall()  # cursor.execute(query)
    # model = models.Leituras.objects.all()
    # model = models.Leituras
    #   context_object_name = 'leituras'
    #   return render('movimentacao/lista_leitura.html', {'leituras': leituras})

    # query = "select  id_morador, mesano from leituras where mesano = '022023'"
    # with connection.cursor() as cursor:
    #     cursor.execute(query)
    #     model = cursor.fetchall()  # cursor.execute(query)

    #     # model = models.Leituras
    #     print('000000000000000000000000000000000000000000000000000000000')
    #     print(model)

    #     template_name = 'movimentacao/lista_leitura.html'
    #     context_object_name = list([model],)  # 'leituras'
