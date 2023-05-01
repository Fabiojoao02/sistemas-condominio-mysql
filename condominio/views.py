from django.contrib.auth.decorators import login_required
from . models import Condominio
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from django.db import connection
from utils import utils
from PIL import Image
from django.views.generic import View
from reportlab.lib.colors import red, black, blue, gray, green

from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.platypus import Table, TableStyle


# tlaves eliminar
# from django.conf import settings
# from django.core.mail import send_mail
# from sendgrid import SendGridAPIClient
# from sendgrid.helpers.mail import Mail
# from .forms import EmailForm
# from django.template.loader import get_template
# from xhtml2pdf import pisa


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


# @login_required(redirect_field_name='redirect_to')
# def geraPDF(request, idb, ma, id_morador):

class GerarPDF(View):

    def get(self, request, ma, id_morador):

        # Cria um objeto HttpResponse com o tipo de conteúdo PDF
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="relatoriocalculospdf.pdf"'

        # Cria o objeto canvas com o objeto HttpResponse
        p = canvas.Canvas(response)

        # Define a fonte e o tamanho da fonte
        p.setFont('Helvetica-Bold', 14)
        # Adiciona o texto ao cabeçalho

        # Define um estilo para as células da primeira coluna
        style = TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),  # Define o nome da fonte
            ('FONTSIZE', (0, 0), (-1, -1), 12),  # Define o tamanho da fonte
            ('TEXTCOLOR', (0, 0), (-1, -1), black),  # Define a cor do texto
            # Define o alinhamento das células da primeira coluna
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ])

        # Executa a consulta SQL bruta e itera sobre os resultados
        with connection.cursor() as cursor:
            cursor.execute(
                '''
                select cal.mesano, 
                    concat(left(cal.mesano,2),'/',right(cal.mesano,4)) as mes_ano,
                    m.apto_sala, cad.nome morador, c.nome conta,
                    ROUND(valor,2) valor
                from calculos cal
                    join contas c on
                    c.id_conta = cal.id_contas
                    join morador m on
                    m.id_morador = cal.id_morador
                    join cadastro cad on
                    cad.id_cadastro = case when responsavel='I' 
                                            then id_inquilino 
                                            else id_proprietario end
                where cal.mesano = %s and m.id_morador = %s
                order by mesano,m.apto_sala,id_contas                
            ''', [ma, id_morador]

            )
            rows = cursor.fetchall()

            y = 750
            linha = 0
            subtotais = {}
            # margem = 50
            total_geral = 0
            apto_sala_anterior = None
            morador_anterior = None
            for row in rows:
                mesano, mes_ano, apto_sala, morador, conta, valor = row
                if apto_sala != apto_sala_anterior:
                    # Adiciona um subtotal para a categoria anterior
                    if apto_sala_anterior:
                        subtotal = subtotais[apto_sala_anterior]
                        p.setFont('Helvetica-Bold', 14)
                        p.drawString(
                            210, y, f'Subtotal...............: {subtotal:.2f}')
                        y -= 20
                    # Adiciona o cabeçalho da categoria
                    # p.drawString(100, 100, '\n\n')
                    p.setFillColor(blue)
                    p.drawString(
                        220, y, f'Apto/Sala: {apto_sala} - {morador} ')
                    p.setFillColor(black)
                    y -= 20
                    p.setFont('Helvetica', 14)
                    apto_sala_anterior = apto_sala
                    morador_anterior = morador
                if linha % 25 == 0 and linha != 0:
                    p.setFont('Helvetica-Bold', 14)
                    p.drawString(
                        150, 765, 'Relatório da Movimentação de contas Mês Ano: '+mes_ano)
                    # p.drawString(100, 100, '\n\n')
                    p.setFont('Helvetica', 14)
                    # Define a cor do texto do cabeçalho
                    # Adiciona uma nova página depois de cada quatro linhas
                    p.drawString(150, y, 'Conta')
                    p.drawString(450, y, 'Valor')
                    p.showPage()
                    p.setFont('Helvetica', 14)
                    y = 750
                if linha % 25 == 0:
                    # Desenha o cabeçalho com fundo colorido
                    # p.drawString(100, 100, '\n\n')
                    p.setFont('Helvetica-Bold', 14)
                    p.drawString(
                        150, 765, 'Relatório da Movimentação de contas Mês Ano: '+mes_ano)
                    # p.drawString(100, 100, '\n\n')
#                    y -= 20
                    p.drawString(150, y, 'Conta')
                    p.drawString(450, y, 'Valor')
                    p.setFont('Helvetica', 14)
                    y -= 20
                # Adiciona os dados ao PDF
                p.drawString(150, y, str(conta))
                # rows.setStyle(style)  # Aplica o estilo à tabela
                p.drawString(
                    450, y, f'{utils.formata_valor(valor)}')
                y -= 20
                # Atualiza os subtotais e total geral
                if apto_sala not in subtotais:
                    subtotais[apto_sala] = 0
                subtotais[apto_sala] += valor
                total_geral += valor
                linha += 1
            # Adiciona o total geral
            p.setFont('Helvetica-Bold', 14)
            # 310, y, f'Total geral..........: {utils.formata_valor(total_geral)}')
            p.drawString(
                150, y, f'Total geral')
            p.drawString(
                450, y, f'{utils.formata_valor(total_geral)}'
            )
            p.setFont('Helvetica', 14)

            p.showPage()
# Movimentação das Leituras

        # Executa a consulta SQL bruta e itera sobre os resultados
        with connection.cursor() as cursor:
            cursor.execute(
                '''
                  select con.nome conta, 
                        concat(left(l.mesano,2),'/',right(l.mesano,4)) as mes_ano,
						cast(l.dt_leitura as date) as dt_leitura ,
						valor_m3, l.leitura_final, l.leitura_inicial,
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
                    where l.id_morador = %s 
                    and l.dt_leitura >= cast(date_add(now(), INTERVAL -12 MONTH) as date) 
                    order by l.id_morador, conta 
                ''', [id_morador]
            )
            rowsl = cursor.fetchall()

            if len(rowsl) > 0:
                y = 750
                linha = 0
                subtotais = {}
                # margem = 50
                total_geral = 0
                conta_anterior = None
                for row in rowsl:
                    conta, mes_ano, dt_leitura, valor_m3, leitura_final, leitura_inicial, consumo_m3,  vl_consumo = row
                    if conta != conta_anterior:
                        # Adiciona um subtotal para a categoria anterior
                        if conta_anterior:
                            subtotal = subtotais[conta_anterior]
                            p.setFont('Helvetica-Bold', 14)
                            p.drawString(
                                210, y, f'Subtotal...............: {subtotal:.2f}')
                            y -= 20
                        # Adiciona o cabeçalho da categoria
                        p.drawString(
                            250, y, str(''))
                        y -= 20
                        p.setFont('Helvetica', 14)
                        conta_anterior = conta
                    if linha % 25 == 0 and linha != 0:
                        p.setFont('Helvetica-Bold', 14)
                        p.drawString(
                            180, 765, 'Extrato leitura de '+conta+' 12 meses anteriores: '+mes_ano)
                        p.setFont('Helvetica', 14)
                        # Define a cor do texto do cabeçalho
                        # Adiciona uma nova página depois de cada quatro linhas
                        # dt_leitura, valor_m3, leitura_final, leitura_inicial, consumo_m3, vl_consumo
                        p.drawString(10, y, 'dt_leitura')
                        p.drawString(40, y, 'valor_m3')
                        p.drawString(70, y, 'leitura_inicial')
                        p.drawString(100, y, 'leitura_final')
                        p.drawString(200, y, 'consumo_m3')
                        p.drawString(300, y, 'vl_consumo')
                        p.showPage()
                        p.setFont('Helvetica', 14)
                        y = 750
                    if linha % 25 == 0:
                        # Desenha o cabeçalho com fundo colorido
                        p.setFont('Helvetica-Bold', 14)
                        p.drawString(
                            180, 765, 'Extrato leitura de '+conta+' 12 meses anteriores: '+mes_ano)
                        p.setFont('Helvetica-Bold', 9)
                        p.drawString(10, y, 'Mês Ano')
                        p.drawString(80, y, 'Data Leitura')
                        p.drawString(150, y, 'Preço M3')
                        p.drawString(230, y, 'Leitura Inicial')
                        p.drawString(330, y, 'Leitura Final')
                        p.drawString(430, y, 'Consumo M3')
                        p.drawString(520, y, 'Valor Consumo')
                    #  p.showPage()
                        y -= 20
                    # Adiciona os dados ao PDF
                    p.setFont('Helvetica', 9)
                    p.drawString(10, y, str(mes_ano))
                    p.drawString(80, y, str(dt_leitura))
                    p.drawString(155, y, str(valor_m3))
                    p.drawString(243, y, str(leitura_inicial))
                    p.drawString(335, y, str(leitura_final))
                    p.drawString(460, y, str(consumo_m3))
                    p.drawString(545, y, f'{utils.formata_valor(vl_consumo)}')

                    y -= 20
                    # Atualiza os subtotais e total geral
                    if conta not in subtotais:
                        subtotais[conta] = 0
                    subtotais[conta] += vl_consumo
                    total_geral += vl_consumo
                    linha += 1

            # Finaliza o PDF e retorna o objeto HttpResponse
            # p.showPage()
            p.save()

        return response
