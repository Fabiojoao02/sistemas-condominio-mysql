from django.views.generic.list import ListView
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
from . import models


class ListaLeitura(ListView):
    def get(self, *args, **kwargs):
        return HttpResponse('Listar')

# model = models.Leituras
# template_name = 'movimentacao/lista_leitura.html'


# @login_required(redirect_field_name='redirect_to')
# def leiturasmes(request, leitura_id):
#    leitura = Leituras.objects.get(id=leitura_id)
#    return render(request, 'movimentacao/leiturasmes.html', {
#        'leitura': leitura
#    })
