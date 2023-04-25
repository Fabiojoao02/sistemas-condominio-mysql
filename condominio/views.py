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
        'condominio1':  Condominio.objects.raw('''
            select c.id_condominio, c.nome nome_condominio
            from condominio c
            where c.id_condominio = ''' + str(id) + '''
        '''),
    }
    # url = reverse('relatorio_calculos_pdf')
    return render(request, 'listacondominio.html', context)


def listaconblomov(request, id):

    # condominio = get_object_or_404(Condominio, id=id)

    context = {
        'condominio':  Condominio.objects.raw('''
            select c.id_condominio, c.nome nome_condominio, b.id_bloco, b.nome nome_bloco
            , concat(left(mesano,2),'/',right(mesano,4)) as mes_ano
            , mesano
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
        'condominio1':  Condominio.objects.raw('''
            select c.id_condominio, c.nome nome_condominio, b.id_bloco, b.nome nome_bloco
            from condominio c
            join bloco b on
            b.id_condominio = c.id_condominio 
            where b.id_bloco = ''' + str(id) + '''
            group by c.id_condominio, c.nome , b.id_bloco, b.nome
            order by b.id_bloco
        '''),
    }
    # url = reverse('relatorio_calculos_pdf')
    return render(request, 'listaconblomov.html', context)


def listaconblomorador(request, idb, ma):

    context = {
        'calculo':  Condominio.objects.raw('''
          select b.id_condominio, m.id_bloco, 
                concat(left(cal.mesano,2),'/',right(cal.mesano,4)) as mes_ano,
                cal.mesano,
                m.apto_sala, m.id_morador,
                cad.nome morador,
                count(*) qde_contas,
                ROUND(sum(valor), 2) valor 
            from calculos cal
                join contas c on
                    c.id_conta=cal.id_contas
                join morador m on
                    m.id_morador=cal.id_morador
                join cadastro cad on
                    cad.id_cadastro=case when responsavel='I' 
                        then id_inquilino else id_proprietario end
                join bloco b on
                    b.id_bloco = m.id_bloco
            where m.id_bloco = %s and cal.mesano = %s
            group by b.id_condominio,m.id_bloco,mesano,m.apto_sala,cad.nome 
            order by cal.mesano, m.id_bloco,m.apto_sala
        ''', [idb, ma]),

        'calculo1':  Condominio.objects.raw('''
            select b.id_condominio, cd.nome nome_condominio, m.id_bloco, 
            b.nome nome_bloco, concat(left(cal.mesano,2),'/',right(cal.mesano,4)) as mes_ano,
                ROUND(sum(valor), 2) valor 
            from calculos cal
                join contas c on
                c.id_conta=cal.id_contas
                join morador m on
                m.id_morador=cal.id_morador
                join cadastro cad on
                cad.id_cadastro=case when responsavel='I' 
                then id_inquilino else id_proprietario end
                join bloco b on
                b.id_bloco = m.id_bloco
                join condominio cd on
                cd.id_condominio = b.id_condominio
            where m.id_bloco = %s and cal.mesano = %s
            group by m.id_bloco,mesano,cd.nome, b.nome 
        ''', [idb, ma]),


    }
    # url = reverse('relatorio_calculos_pdf')
    return render(request, 'listaconblomorador.html', context)


def listaconta(request, idb, ma, id_morador):

    context = {
        'conta':  Condominio.objects.raw('''
          select b.id_condominio, m.id_bloco, 
                concat(left(cal.mesano,2),'/',right(cal.mesano,4)) as mes_ano,
                cal.mesano,
                m.apto_sala,
                cad.nome morador,
                c.id_conta, c.nome nome_conta,
                ROUND(valor, 2) valor 
            from calculos cal
                join contas c on
                    c.id_conta=cal.id_contas
                join morador m on
                    m.id_morador=cal.id_morador
                join cadastro cad on
                    cad.id_cadastro=case when responsavel='I' 
                        then id_inquilino else id_proprietario end
                join bloco b on
                    b.id_bloco = m.id_bloco
            where m.id_bloco = %s and cal.mesano = %s and m.id_morador = %s
            order by cal.mesano, m.id_bloco,nome_conta
        ''', [idb, ma, id_morador]),

        'conta1':  Condominio.objects.raw('''
          select distinct b.id_condominio, cd.nome nome_condominio, m.id_bloco,
                b.nome nome_bloco, 
                concat(left(cal.mesano,2),'/',right(cal.mesano,4)) as mes_ano,
                cal.mesano,
                m.apto_sala,
                cad.nome morador,
                ROUND(sum(valor),2) valor
            from calculos cal
                join contas c on
                    c.id_conta=cal.id_contas
                join morador m on
                    m.id_morador=cal.id_morador
                join cadastro cad on
                    cad.id_cadastro=case when responsavel='I' 
                        then id_inquilino else id_proprietario end
                join bloco b on
                    b.id_bloco = m.id_bloco
                join condominio cd on
                cd.id_condominio = b.id_condominio
            where m.id_bloco = %s and cal.mesano = %s and m.id_morador = %s
            group by b.id_condominio, cd.nome , m.id_bloco,b.nome,cal.mesano,
                m.apto_sala,cad.nome
            
        ''', [idb, ma, id_morador]),
    }
    # url = reverse('relatorio_calculos_pdf')
    return render(request, 'listaconta.html', context)
