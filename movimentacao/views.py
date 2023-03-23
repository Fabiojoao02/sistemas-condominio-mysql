from django.views.generic.list import ListView
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
from . import models


class ListaLeitura(ListView):
    model = models.Leituras
    template_name = 'movimentacao/lista_leitura.html'
    context_object_name = 'leituras'
