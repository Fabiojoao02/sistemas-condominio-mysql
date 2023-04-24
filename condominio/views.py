from django.contrib.auth.decorators import login_required
from . models import Condominio
from django.shortcuts import render, redirect, get_object_or_404


# @login_required(redirect_field_name='redirect_to')
def index(request):

    context = {
        'nome_pagina': 'Início da dashboard',
        'listcondo':  Condominio.objects.raw('''
        select c.id_condominio, c.nome nome_condominio, cidade,bairro,estado
        from condominio c
        order by nome_condominio
    ''')
    }
    return render(request, 'index.html', context)

# @login_required(redirect_field_name='redirect_to')


def listacondominio(request, id):

    # condominio = get_object_or_404(Condominio, id=id)

    context = {
        'condominio':  Condominio.objects.raw('''
            select c.id_condominio, c.nome nome_condominio, id_bloco, b.nome nome_bloco 
            from condominio c
            join bloco b on
            b.id_condominio = c.id_condominio 
            where c.id_condominio = ''' + str(id) + '''
            order by id_bloco
        '''),
    }
    # url = reverse('relatorio_calculos_pdf')
    return render(request, 'listacondominio.html', context)


def listaconblomorador(request, id):

    # condominio = get_object_or_404(Condominio, id=id)

    context = {
        'condominio':  Condominio.objects.raw('''
            select c.id_condominio, c.nome nome_condominio, b.id_bloco, b.nome nome_bloco
            , concat(left(mesano,2),'/',right(mesano,4)) as mesano
            , ROUND(sum(valor),2) valor_total
            from condominio c
            join bloco b on
            b.id_condominio = c.id_condominio 
            join movimento mov on
            mov.id_bloco = b.id_bloco
            where b.id_bloco = ''' + str(id) + '''
            group by c.id_condominio, c.nome , b.id_bloco, b.nome ,mov.mesano
            order by b.id_bloco
        '''),
    }
    # url = reverse('relatorio_calculos_pdf')
    return render(request, 'listaconblomorador.html', context)
