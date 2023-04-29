from django.contrib.auth.decorators import login_required
from . models import Condominio
from django.shortcuts import render, redirect, get_object_or_404


@login_required(redirect_field_name='redirect_to')
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


@login_required(redirect_field_name='redirect_to')
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


@login_required(redirect_field_name='redirect_to')
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


@login_required(redirect_field_name='redirect_to')
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


@login_required(redirect_field_name='redirect_to')
def listaconta(request, idb, ma, id_morador):

    context = {
        'conta':  Condominio.objects.raw('''
          select b.id_condominio, m.id_bloco, 
                concat(left(cal.mesano,2),'/',right(cal.mesano,4)) as mes_ano,
                cal.mesano,
                m.apto_sala,
                cad.nome morador,m.id_morador, 
                c.id_conta, c.nome nome_conta,
                case when cal.id_contas in (select id_contas from leituras 
                    where mesano = cal.mesano and 
                        id_morador = cal.id_morador and 
                        id_conta = cal.id_contas) 
                    then 1 else 0 
                    end tem_leitura,
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
                cad.nome morador,m.id_morador,
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

        'leitura':  Condominio.objects.raw('''
            select  c.id_condominio, c.nome nome_condominio, b.id_bloco, 
                concat(left(l.mesano,2),'/',right(l.mesano,4)) as mes_ano,
                b.nome nome_bloco, m.apto_sala, cad.nome morador, l.mesano, 
                con.id_conta, con.nome conta, l.dt_leitura, valor_m3, 
                l.leitura_final, l.leitura_inicial,
                ROUND((l.leitura_final - l.leitura_inicial),2) consumo_m3,
                ROUND((l.leitura_final - l.leitura_inicial)*valor_m3,2) vl_consumo
            from leituras l
            join morador m on
                m.id_morador = l.id_morador
            join cadastro cad on
                cad.id_cadastro = case when responsavel='I' then id_inquilino else id_proprietario end
            join bloco b on
                b.id_bloco = m.id_bloco
            join condominio c on
                c.id_condominio = b.id_condominio
            join contas con on
                con.id_conta = l.id_contas
            where b.id_bloco = %s and l.id_morador = %s and l.mesano = %s
            order by l.id_morador, conta , l.mesano          
        ''', [idb, id_morador, ma]),

    }
    # url = reverse('relatorio_calculos_pdf')
    return render(request, 'listaconta.html', context)


@login_required(redirect_field_name='redirect_to')
def listaleitura(request, idb, ma, id_morador):

    context = {
        'leitura':  Condominio.objects.raw('''
            select  c.id_condominio, c.nome nome_condominio, b.id_bloco, 
                concat(left(l.mesano,2),'/',right(l.mesano,4)) as mes_ano,
                b.nome nome_bloco, m.apto_sala, cad.nome morador, l.mesano, 
                con.id_conta, con.nome conta, l.dt_leitura, valor_m3, 
                l.leitura_final, l.leitura_inicial,l.id_morador, 
                ROUND((l.leitura_final - l.leitura_inicial),2) consumo_m3,
                ROUND((l.leitura_final - l.leitura_inicial)*valor_m3,2) vl_consumo
            from leituras l
            join morador m on
                m.id_morador = l.id_morador
            join cadastro cad on
                cad.id_cadastro = case when responsavel='I' then id_inquilino else id_proprietario end
            join bloco b on
                b.id_bloco = m.id_bloco
            join condominio c on
                c.id_condominio = b.id_condominio
            join contas con on
                con.id_conta = l.id_contas
            where b.id_bloco = %s and l.id_morador = %s 
            and l.dt_leitura >= cast(date_add(now(), INTERVAL -12 MONTH) as date) 
            order by l.id_morador, conta , l.mesano          
        ''', [idb, id_morador]),

    }
    # url = reverse('relatorio_calculos_pdf')
    return render(request, 'listaleitura.html', context)
