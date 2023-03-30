# from django.views.generic.list import ListView
from django.views.generic import TemplateView
# from django.shortcuts import render, redirect, reverse
# from django.http import HttpResponse
from django.contrib import messages
# from django.views import View
from . models import Leituras
from django.db import connection
# from django.db.models import Count


class ListaLeitura(TemplateView):
    template_name = 'movimentacao/lista_leitura.html'
    paginate_by = 2

    def get_context_data(self, **kwargs):
        context = super(ListaLeitura, self).get_context_data(**kwargs)
        context = {
            'leituras':  Leituras.objects.raw("\
            select concat(left(mesano,2),'/',right(mesano,4)) as mesano \
                , id_leituras as id_leituras, \
                m.apto_sala as Apto_Sala, \
                cad.nome morador, c.nome as Conta, vl_gas_m3, \
                leitura_inicial, leitura_final, \
                ROUND((leitura_final - leitura_inicial),3) as Consumo_m3, \
                ROUND(((leitura_final - leitura_inicial) * vl_gas_m3),2) Valor,\
                cast(dt_leitura as date) dt_leitura \
            from leituras  l \
            join morador m on \
                m.id_morador = l.id_morador  \
            join cadastro cad on \
                cad.id_cadastro = id_inquilino \
            join contas c on \
                c.id_conta = l.id_contas \
        ")
        }
        return context
