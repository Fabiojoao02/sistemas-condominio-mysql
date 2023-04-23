from django.contrib.auth.decorators import login_required
from . models import Condominio
from django.shortcuts import render, redirect


# @login_required(redirect_field_name='redirect_to')
def index(request):

    context = {
        'nome_pagina': 'Início da dashboard',
        'listcondo':  Condominio.objects.raw('''
        select c.id_condominio, c.nome nome_condominio, cidade,bairro,estado,
        id_bloco, b.nome nome_bloco
        from condominio c
        join bloco b on
        b.id_condominio = c.id_condominio 
        order by id_bloco
    ''')
    }
    return render(request, 'index.html', context)

#@login_required(redirect_field_name='redirect_to')
def listacondominio(request, id):
    context = {
        'calculos':  Condominio.objects.raw('''
            select c.id_condominio, c.nome nome_condominio, id_bloco, b.nome nome_bloco 
            from condominio c
            join bloco b on
            b.id_condominio = c.id_condominio 
            where id_condominio = ''' + str(id) + '''
            order by id_bloco
        ''')
    }
    # url = reverse('relatorio_calculos_pdf')
    return render(request, 'listacondominio.html', context)
