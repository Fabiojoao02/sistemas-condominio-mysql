from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from django.contrib import messages
# from django.views import View
from . models import Leituras
from django.db import connection
# from django.db.models import Count


# class ListaLeitura(DetailView):
# def get(self, *args, **kwargs):
#     messages.error(self.request, 'Erro de teste...')
#     return redirect(self.request.META[HTTP_REFERER])


def dictfetchall(cursor):
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]


def listaleitura(request):
    cursor = connection.cursor()
    cursor.execute("\
            select concat(left(mesano,2),'/',right(mesano,4)) as mesano \
                , id_leituras as id_leituras, \
                l.id_morador as id_morador, \
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
    model = dictfetchall(cursor)
    paginate_by = 2
    return render(request, 'movimentacao/lista_leitura.html', {'leituras': model})
