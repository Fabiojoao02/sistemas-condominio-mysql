from django.contrib.auth.decorators import login_required
from . models import Condominio
from django.shortcuts import render, redirect


@login_required(redirect_field_name='redirect_to')
def listacondominio(request, id=None, *args, **kwargs):

    context = {
        'calculos':  Condominio.objects.raw('''
            select c.id_condominio, c.nome, id_bloco, b.nome 
            from condominio c
            join bloco b on
            b.id_condominio = c.id_condominio 
            where id_condominio = ''' + str(id) + '''
            order by id_bloco
        ''')
    }
    # url = reverse('relatorio_calculos_pdf')
    return context
