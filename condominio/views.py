import os
from django.contrib.auth.decorators import login_required
from . models import Condominio
from movimentacao.models import Calculos, Leituras, Movimento
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from django.db import connection
from utils import utils
# from PIL import Image
from django.views.generic import View
from reportlab.lib.colors import red, black, blue, gray, green
from django.contrib import messages
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.platypus import Table, TableStyle, Image
from pathlib import Path
from emailer.views import sendemail
from pixqrcodegen import Payload

# graficos
# import math
import random
from reportlab.graphics.charts.piecharts import Pie
from reportlab.graphics.charts.legends import Legend
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.graphics.shapes import Drawing, String, Line, Wedge
from reportlab.graphics.charts.barcharts import VerticalBarChart
# from reportlab.graphics.charts.barcharts import BarChart
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas
from reportlab.graphics import renderPDF
from reportlab.lib.colors import Color, PCMYKColor
from reportlab.graphics.charts.barcharts import HorizontalBarChart
from reportlab.graphics.shapes import Drawing, String
from reportlab.pdfbase.pdfmetrics import stringWidth
from movimentacao.forms import AutorizaCalculoForm


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
            select 
            c.id_condominio, c.nome nome_condominio, b.id_bloco, b.nome nome_bloco
            , concat(left(mov.mesano,2),'/',right(mov.mesano,4)) as mes_ano
            , cal.mesano mesano_cal, mov.mesano mesano
            , (select ROUND(sum(m.valor),2) from movimento m where m.id_bloco = mov.id_bloco and m.mesano = mov.mesano) valor_total  
            from condominio c
            join bloco b on
            b.id_condominio = c.id_condominio 
            join movimento mov on
            mov.id_bloco = b.id_bloco
            left join calculos cal on
            cal.mesano = mov.mesano and
            cal.id_bloco = mov.id_bloco
            where b.id_bloco = ''' + str(id) + '''
            group by c.id_condominio, c.nome , b.id_bloco, b.nome ,cal.mesano
            order by mov.mesano
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
            select b.id_condominio, cd.nome nome_condominio, m.id_bloco, cal.mesano,
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


@login_required(redirect_field_name='redirect_to')
def calcularmovimentacao(request, idb, ma):

    # condominio = get_object_or_404(Condominio, id=id)

    context = {
        'calcmov':  Condominio.objects.raw('''
                select distinct c.id_condominio, mov.mesano,
                    concat(left(mesano,2),'/',right(mesano,4)) as mes_ano,
                    mov.id_contas, ct.nome conta, valor,
                    (select count(m.id_morador) qde
                    FROM bloco b1
                    JOIN morador m ON m.id_bloco = b1.id_bloco
                    where m.situacao = 'A'  and b1.id_bloco = b.id_bloco) nr_condomiminos,
                    (select sum(m.qt_moradores) soma
                    FROM bloco b1
                    JOIN morador m ON m.id_bloco = b1.id_bloco
                    where m.situacao = 'A' and b1.id_bloco = b.id_bloco) qde_moradores
                    from condominio c
                    join bloco b on
                    b.id_condominio = c.id_condominio 
                    join movimento mov on
                    mov.id_bloco = b.id_bloco
                    join contas ct on
                    ct.id_conta = mov.id_contas
                    where b.id_bloco = %s and mesano = %s
                order by conta
        ''', [idb, ma]),

        'calcmov1':  Condominio.objects.raw('''
                select distinct c.id_condominio, c.nome nome_condominio,
                    b.id_bloco, b.nome nome_bloco, mov.mesano,
                    case when mov.situacao='A' then 'Aberto'
                        when mov.situacao='M' then 'Movimentação'
                        when mov.situacao='F' then 'Fechado' end situacao,
                    concat(left(mesano,2),'/',right(mesano,4)) as mes_ano,
                    ROUND(sum(valor),2)  valor_total,
                    ROUND(sum(valor),2)  +
					ifnull((SELECT  sum(ROUND((leitura_final-leitura_Inicial) * valor_m3,2)) as valor_total_leitura 
                            from leituras l
                            join contas ct on
                                ct.id_conta = l.id_contas
                            where mesano = mov.mesano),0) valor_total_leitura,  
                    (select count(m.id_morador) qde
                    FROM bloco b1
                    JOIN morador m ON m.id_bloco = b1.id_bloco
                    where m.situacao = 'A'  and b1.id_bloco = b.id_bloco) nr_condomiminos,
                    (select sum(m.qt_moradores) soma
                    FROM bloco b1
                    JOIN morador m ON m.id_bloco = b1.id_bloco
                    where m.situacao = 'A' and b1.id_bloco = b.id_bloco) qde_moradores
                    from condominio c
                    join bloco b on
                    b.id_condominio = c.id_condominio 
                    join movimento mov on
                    mov.id_bloco = b.id_bloco
                    where b.id_bloco = %s and mesano = %s
                    group by c.id_condominio, c.nome, b.id_bloco, b.nome , mov.mesano
             ''', [idb, ma]),
        'lei':  Leituras.objects.raw('''
                SELECT id_leituras, mesano, id_contas ,nome conta, sum(ROUND((leitura_final-leitura_Inicial) * valor_m3,2)) as total_leituras
                ,concat(left(mesano,2),'/',right(mesano,4)) as mes_ano,l.id_bloco
                from leituras l
                join contas ct on
                ct.id_conta = l.id_contas and leituras = 1
                where l.id_bloco = %s and l.mesano = %s
                group by l.mesano, id_contas ,nome,l.id_bloco 
             ''', [idb, ma]),
        'lei1':  Leituras.objects.raw('''
                 SELECT  id_leituras, mov.mesano #,SUM(ROUND((leitura_final-leitura_Inicial) * valor_m3,2)) as total_leituras
				,mov.id_bloco id_bloco_mov
                ,(select sum(ROUND((leitura_final-leitura_Inicial) * valor_m3,2)) totl from leituras le  where le.id_bloco = mov.id_bloco and le.mesano =mov.mesano )as total_leituras
                ,concat(left(l.mesano,2),'/',right(l.mesano,4)) as mes_ano
                ,(SELECT GROUP_CONCAT(nome SEPARATOR ', ') AS leituras
                    FROM contas where leituras=1 
                    GROUP BY leituras) agrupador
                from movimento mov 
                left join leituras l on
                mov.mesano = l.mesano and
                mov.id_bloco = l.id_bloco
                left join contas ct on
                ct.id_conta = l.id_contas and leituras = 1
                where mov.id_bloco = %s and mov.mesano = %s
                group by mov.mesano,mov.id_bloco
        ''', [idb, ma]),
        'idb': idb, 'ma': ma
    }

    # executa a proc para calcular os rateios
    form = AutorizaCalculoForm()
    if request.method == 'POST':
        form = AutorizaCalculoForm(request.POST)
        with connection.cursor() as cursor:
            cursor.callproc('prc_calcula_movimento', [ma, idb])
            cursor.execute('COMMIT')

            messages.success(request, 'Calculo gerado com sucesso')

    return render(request, 'calcularmovimentacao.html', context)


class GerarPDF(View):

    def get(self, request, ma, id_morador, idb):

        caminho_imagem = Path(__file__).parent
       # Define o caminho do arquivo
        caminho_arquivo = Path(__file__).parent.parent
        caminho_imagem = caminho_arquivo / 'pixqrcodegen.png'
        # imagem = Image(caminho_imagem)
        # print(caminho_imagem)
        arquivo = caminho_arquivo / 'emailer' / \
            'templates' / 'emailer' / f'{ma}'

        # cria a pasta do mes/ano corespondente
        arquivo.mkdir(exist_ok=True)

        # Cria um objeto HttpResponse com o tipo de conteúdo PDF
        response = HttpResponse(content_type='application/pdf')
        # nesse comando abaixo abre um pop para definir o local para salvar
        # response['Content-Disposition'] = 'attachment; filename="relatoriocalculospdf.pdf"'

        # Cria o objeto canvas com o objeto HttpResponse
        # case usar o comando acima abre um pop para definir o local para salvar
        # p = canvas.Canvas(response)
        p = canvas.Canvas('relatoriocalculospdf.pdf')

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
                select b.id_condominio, cal.mesano, 
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
					join bloco b on
                    b.id_bloco = m.id_bloco                                            
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
                id_condominio, mesano, mes_ano, apto_sala, morador, conta, valor = row
                if apto_sala != apto_sala_anterior:
                    # Adiciona um subtotal para a categoria anterior
                    if apto_sala_anterior:
                        subtotal = subtotais[apto_sala_anterior]
                        p.setFont('Helvetica-Bold', 14)
                        p.drawAlignedString(
                            210, y, f'Subtotal...............: {subtotal:.2f}')
                        y -= 20
                    # Adiciona o cabeçalho da categoria
                    # p.drawString(100, 100, '\n\n')
                    p.setFillColor(blue)
                    p.drawString(
                        150, y, f'Apto/Sala: {apto_sala} - {morador} ')
                    p.setFillColor(black)
                    y -= 20
                    p.setFont('Helvetica', 14)
                    apto_sala_anterior = apto_sala
                    morador_anterior = morador
                if linha % 25 == 0 and linha != 0:
                    p.setFont('Helvetica-Bold', 14)
                    p.drawString(
                        150, 765, 'Demonstrativo das contas Mês Ano: '+mes_ano)
                    # p.drawString(100, 100, '\n\n')
                    p.setFont('Helvetica', 14)
                    # Define a cor do texto do cabeçalho
                    # Adiciona uma nova página depois de cada quatro linhas
                    p.drawString(150, y, 'Conta')
                    p.drawAlignedString(450, y, 'Valor')
                    p.showPage()
                    p.setFont('Helvetica', 14)
                    y = 750
                if linha % 25 == 0:
                    # Desenha o cabeçalho com fundo colorido
                    # p.drawString(100, 100, '\n\n')
                    p.setFont('Helvetica-Bold', 14)
                    p.drawString(
                        150, 765, 'Demonstrativo das contas Mês Ano: '+mes_ano)
                    # p.drawString(100, 100, '\n\n')
#                    y -= 20
                    p.drawString(150, y, 'Conta')
                    p.drawAlignedString(450, y, 'Valor')
                    p.setFont('Helvetica', 14)
                    y -= 20
                # Adiciona os dados ao PDF
                p.drawString(150, y, str(conta))
                # rows.setStyle(style)  # Aplica o estilo à tabela
                p.drawAlignedString(
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
            p.drawAlignedString(
                450, y, f'{utils.formata_valor(total_geral)}'
            )
            p.setFont('Helvetica', 14)

        # Detalhamento das conta no mesano - Movimentação

        with connection.cursor() as cursor:
            cursor.execute(
                '''
                select m.mesano, id_bloco , id_contas, nome, valor, mensagem,
                concat(cast(id_contas as char(30)),'-', nome) cod_nome,
                concat(left(m.mesano,2),'/',right(m.mesano,4)) as mes_ano
                from movimento m
                left join movimento_msg msg on
                    msg.mesano = m.mesano
                join  contas c on
                    c.id_conta = m.id_contas
                where id_bloco = %s and m.mesano = %s
                ''', [idb, ma]
            )
            rowsm = cursor.fetchall()
            p.setFillColor(green)
            if len(rowsm) > 0:
                y -= 20
               # y = 950
                linha = 0
                subtotais = {}
                # margem = 50
                total_geral_mov = 0
                mesano_anterior = None
                for row in rowsm:
                    mesano, id_bloco, id_contas, nome, valor, mensagem, cod_nome, mes_ano = row
                    if mesano != mesano_anterior:
                        # Adiciona um subtotal para a categoria anterior
                        if mesano_anterior:
                            subtotal = subtotais[mesano_anterior]
                            p.setFont('Helvetica-Bold', 12)
                            p.drawAlignedString(
                                210, y, f'Subtotal...............: {subtotal:.2f}')
                            y -= 10
                        # Adiciona o cabeçalho da categoria
                        p.drawString(
                            250, y, str(''))
                        y -= 15
                        p.setFont('Helvetica', 12)
                        mesano_anterior = mesano
                    if linha % 25 == 0 and linha != 0:
                        p.setFont('Helvetica-Bold', 12)
                        p.drawString(
                            150, y, 'Relação das despesas geral')
                        p.setFont('Helvetica', 12)
                        y -= 15
                        # Define a cor do texto do cabeçalho
                        # Adiciona uma nova página depois de cada quatro linhas
                        # dt_leitura, valor_m3, leitura_final, leitura_inicial, consumo_m3, vl_consumo
                        p.drawString(155, y, 'Conta')
                        p.drawAlignedString(380, y, 'valor')
                        p.showPage()
                        p.setFont('Helvetica', 12)
                        # y = 750
                    if linha % 25 == 0:
                        # Desenha o cabeçalho com fundo colorido
                        p.setFont('Helvetica-Bold', 12)
                        p.drawString(
                            150, y, 'Relação das despesas geral')
                        y -= 15
                        p.setFont('Helvetica-Bold', 9)
                        p.drawString(155, y, 'Conta')
                        p.drawAlignedString(380, y, 'Valor')
                    #  p.showPage()
                        y -= 15
                    # Adiciona os dados ao PDF
                    p.setFont('Helvetica', 9)
                    p.drawString(155, y, str(cod_nome))
                    p.drawRightString(
                        380, y, f'{utils.formata_valor(valor)}')
                    # p.drawRightString(300, y, f'{utils.formata_valor(valor)}')
                    # p.drawString(300, y, f'{utils.formata_valor(valor)}')

                    y -= 15
                    # Atualiza os subtotais e total geral
                    if mesano not in subtotais:
                        subtotais[mesano] = 0
                    subtotais[mesano] += valor
                    total_geral_mov += valor
                    linha += 1

                p.setFont('Helvetica-Bold', 9)
                p.drawString(
                    150, y, f'Total geral')
                p.drawAlignedString(
                    350, y, f'{utils.formata_valor(total_geral_mov)}')
                p.setFont('Helvetica', 9)

            # Finaliza o PDF e retorna o objeto HttpResponse
            # finaliza o detalhamento
            p.setFillColor(black)
            # Adiciona a imagem ao conteúdo do PDF
            # adiciona o QRCODE
            qrcode(request, f'{round(total_geral,2)}', id_condominio)
            # Adicionando a imagem

            p.drawImage(caminho_imagem,
                        x=10, y=700, width=130, height=130)

            # p.drawImage(caminho_imagem,
            #           x=400, y=y, width=150, height=150)

            # final do QRCODE
            y -= 25
            if mensagem:
                p.setFillColor(red)
                p.setFont('Helvetica-Bold', 12)
                p.drawString(150, y, 'Mensagem aos condôminos')
                p.setFillColor(black)
                p.setFont('Helvetica', 10)
                y -= 15
                p.drawString(150, y, str(mensagem))

        # graficos
        # Executa a consulta SQL bruta e itera sobre os resultados
        separador = '%'
        with connection.cursor() as cursor:
            cursor.execute(
                """
				      select concat(c.nome,'-',
                        CAST(ROUND((valor/
                        (select sum(valor) from calculos c1
                            where c1.mesano = cal.mesano  and c1.id_morador = cal.id_morador)*100),0) 
                            as varchar(50)),%s) Conta,
                        ROUND(valor,2) valor
                	    from calculos cal
                    	join contas c on
                        c.id_conta = cal.id_contas
                		where cal.mesano = %s and cal.id_morador = %s
            """, [([separador]), ma, id_morador]

            )
            dados = cursor.fetchall()
            # *********************************Grafica de Barras
            # Cria o gráfico de barras verticais
            y -= 200
            # Criando o objeto Drawing para conter o gráfico
            # Criando a lista de labels e valores a partir dos dados da query
            labels = [label for label, _ in dados]
            valores = [valor for _, valor in dados]

            # Criando o objeto Drawing para conter o gráfico
            d = Drawing(400, 200)

            # Configurando o gráfico de barras verticais
            chart = VerticalBarChart()
            chart.x = 50
            chart.y = 30
            chart.height = 100
            chart.width = 300
            chart.data = [valores]
            chart.categoryAxis.categoryNames = labels
            chart.valueAxis.valueMin = 0
            chart.valueAxis.valueMax = max(valores) + 10
            chart.valueAxis.valueStep = 50
            chart.bars.strokeColor = colors.black
            # Girar os rótulos verticalmente
            chart.categoryAxis.labels.angle = 90

            # Função para gerar uma cor aleatória
            # Definindo as cores aleatórias para as barras
            for i, data in enumerate(chart.data):
                for j, value in enumerate(data):
                    bar = chart.bars[(i, j)]
                    bar.fillColor = colors.Color(
                        random.random(), random.random(), random.random())

            # Adicionando os valores sobre os rótulos de barra
            for i, data in enumerate(chart.data):
                for j, value in enumerate(data):
                    x = chart.x + j * (chart.width / len(data)) + \
                        (chart.width / len(data)) / 2
                    y = chart.y + chart.height + 10
                    # label = String(x, y, str(value))
                    label = String(x, y, f'{utils.formata_valor(value)}')

                    label.fontName = 'Helvetica'
                    label.fontSize = 10
                    label.textAnchor = 'middle'
                    d.add(label)

                    # Adicionando o gráfico ao objeto Drawing
            d.add(chart)
            renderPDF.draw(d, p, 100, y)
            # *********************************FIM Grafica de Barras
            # *********************************Grafica de Pizza
        with connection.cursor() as cursor:
            cursor.execute(
                """
				      select distinct cast(c.id_conta as char(3)) conta,
                        ROUND(valor,2) valor
                	    from calculos cal
                    	join contas c on
                        c.id_conta = cal.id_contas
                		where cal.mesano = %s and cal.id_morador = %s
            """, [ma, id_morador]

            )
            dados = cursor.fetchall()

            # Cria o gráfico de barras verticais
            y -= 20
            pc = Pie()
            pc.x = 100  # 65
            pc.y = 400
            pc.width = 110
            pc.height = 110
            pc.data = [value for _, value in dados]
            pc.labels = [label for label, _ in dados]
            pc.slices.strokeWidth = 0.5
            pc.slices[0].popout = 10
            pc.slices[0].fontColor = colors.black

            d = Drawing(100, y)
            d.add(pc)
            renderPDF.draw(d, p, 330, 1)

            # *********************************FIM Grafico de Pizza

           # p.showPage()
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
                    order by l.mesano, l.id_morador, conta 
                ''', [id_morador]
            )
            rowsl = cursor.fetchall()

            if len(rowsl) > 0:
                p.showPage()
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
                            p.drawAlignedString(
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
                            180, 765, 'Extrato leitura de '+conta+' 12 meses anteriores')
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
                            180, 765, 'Extrato leitura de '+conta+' 12 meses anteriores')
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
                    p.drawAlignedString(
                        175, y, f'{utils.formata_valor(valor_m3)}')
                    p.drawAlignedString(270, y, str(leitura_inicial))
                    p.drawAlignedString(365, y, str(leitura_final))
                    p.drawAlignedString(470, y, str(consumo_m3))
                    p.drawRightString(
                        575, y, f'{utils.formata_valor(vl_consumo)}')

                    y -= 20
                    # Atualiza os subtotais e total geral
                    if conta not in subtotais:
                        subtotais[conta] = 0
                    subtotais[conta] += vl_consumo
                    total_geral += vl_consumo
                    linha += 1

                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        select concat(left(l.mesano,2),'/',right(l.mesano,4)) as mes_ano,
                                ROUND((l.leitura_final - l.leitura_inicial),2) consumo_m3
                            from leituras l
                            join morador m on
                                m.id_morador = l.id_morador
                            join contas con on
                                con.id_conta = l.id_contas
                            where l.id_morador = %s
                            and l.dt_leitura >= cast(date_add(now(), INTERVAL -12 MONTH) as date) 
                            order by l.mesano, l.id_morador
                    """, [id_morador]

                    )
                    dados = cursor.fetchall()

                    # dados = [('01/2023', 50)  # , ('02/2023', 30),
                    # ('03/2023', 20), ('04/2023', 40),
                    # ('05/2023', 10), ('06/2023', 40),
                    # ('07/2023', 25), ('08/2023', 80),
                    # ('09/2023', 15), ('10/2023', 20),
                    # ('11/2023', 20), ('12/2023', 90),
                    # ]
                    # *********************************Grafica de Barras
                    # Cria o gráfico de barras verticais
                    y -= 300
                    # Criando o objeto Drawing para conter o gráfico
                    # Criando a lista de labels e valores a partir dos dados da query
                    labels = [label for label, _ in dados]
                    valores = [valor for _, valor in dados]

                    # len(dados)
                    # Criando o objeto Drawing para conter o gráfico
                    d = Drawing(400, 200)

                    # Configurando o gráfico de barras verticais
                    chart = VerticalBarChart()
                    chart.x = 50
                    chart.y = 130
                    chart.height = 100
                    chart.width = 400
                    chart.data = [valores]
                    chart.categoryAxis.categoryNames = labels
                    chart.valueAxis.valueMin = 0
                    chart.valueAxis.valueMax = max(valores) + 10
                    chart.valueAxis.valueStep = 50
                    chart.bars.strokeColor = colors.black
                    # Girar os rótulos verticalmente
                    if len(dados) <= 10:
                        chart.categoryAxis.labels.angle = 0
                    else:
                        chart.categoryAxis.labels.angle = 90

                    # Função para gerar uma cor aleatória
                    # Definindo as cores aleatórias para as barras
                    for i, data in enumerate(chart.data):
                        for j, value in enumerate(data):
                            bar = chart.bars[(i, j)]
                            bar.fillColor = colors.Color(
                                random.random(), random.random(), random.random())

                    # Adicionando os valores sobre os rótulos de barra
                    for i, data in enumerate(chart.data):
                        for j, value in enumerate(data):
                            x = chart.x + j * (chart.width / len(data)) + \
                                (chart.width / len(data)) / 2
                            y = chart.y + chart.height + 10
                            # label = String(x, y, str(value))
                            label = String(
                                x, y, f'{utils.formata_valor(value)}')

                            label.fontName = 'Helvetica'
                            label.fontSize = 10
                            label.textAnchor = 'middle'
                            d.add(label)

                            # Adicionando o gráfico ao objeto Drawing
                    d.add(chart)
                    renderPDF.draw(d, p, 80, y)
                # fim controle grafico leituras

            # 3 pagina do PDF caso o condômino tenha movimentação de leituras
            p.showPage()
            p.setFont('Helvetica-Bold', 16)
            p.drawString(
                180, 765, 'Analise dos 12 meses anteriores')

            # inicio grafica analise geral de meses 12 do condômino
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    select concat(left(cal.mesano,2),'/',right(cal.mesano,4)) as mes_ano,
                        ROUND(sum(valor),2) valor
                    from calculos cal
                    join contas con on
                        con.id_conta = cal.id_contas
                    where cal.id_morador = %s and
                        concat(right(cal.mesano,4),left(cal.mesano,2)) >= 
                    replace(left(cast(date_add(now(), INTERVAL -12 MONTH) as date),7),'-','')
                    group by cal.mesano
                    order by cal.mesano
                """, [id_morador]

                )
                dados = cursor.fetchall()

                # dados = [('01/2023', 50), ('02/2023', 30),
                #         ('03/2023', 20), ('04/2023', 40),
                #         ('05/2023', 10), ('06/2023', 40),
                #         ('07/2023', 25), ('08/2023', 80),
                #         ('09/2023', 15), ('10/2023', 20),
                #         ('11/2023', 20), ('12/2023', 90),
                #         ]
                # *********************************Grafica de Barras
                # Cria o gráfico de barras verticais
                y -= 300
                # Criando o objeto Drawing para conter o gráfico
                # Criando a lista de labels e valores a partir dos dados da query
                labels = [label for label, _ in dados]
                valores = [valor for _, valor in dados]

                # len(dados)
                # Criando o objeto Drawing para conter o gráfico
                d = Drawing(400, 200)

                # Configurando o gráfico de barras verticais
                chart = VerticalBarChart()
                chart.x = 50
                chart.y = 130
                chart.height = 150
                chart.width = 500
                chart.data = [valores]
                chart.categoryAxis.categoryNames = labels
                chart.valueAxis.valueMin = 0
                chart.valueAxis.valueMax = max(valores) + 10
                chart.valueAxis.valueStep = 50
                chart.bars.strokeColor = colors.black
                # Girar os rótulos verticalmente
                # if len(dados) <= 10:
                #   chart.categoryAxis.labels.angle = 0
                # else:
                chart.categoryAxis.labels.angle = 0

                # Função para gerar uma cor aleatória
                # Definindo as cores aleatórias para as barras
                for i, data in enumerate(chart.data):
                    for j, value in enumerate(data):
                        bar = chart.bars[(i, j)]
                        bar.fillColor = colors.Color(
                            random.random(), random.random(), random.random())

                # Adicionando os valores sobre os rótulos de barra
                for i, data in enumerate(chart.data):
                    for j, value in enumerate(data):
                        x = chart.x + j * (chart.width / len(data)) + \
                            (chart.width / len(data)) / 2
                        y = chart.y + chart.height + 10
                        # label = String(x, y, str(value))
                        label = String(
                            x, y, f'{utils.formata_valor(value)}')

                        label.fontName = 'Helvetica'
                        label.fontSize = 10
                        label.textAnchor = 'middle'
                        d.add(label)

                        # Adicionando o gráfico ao objeto Drawing
                d.add(chart)
                renderPDF.draw(d, p, 10, y)

            # fim controle grafico de 12 meses do condômino

            # Finaliza o PDF e retorna o objeto HttpResponse
            # finaliza o detalhamento

            p.save()
            nome_arquivo = arquivo / f'{apto_sala_anterior}.pdf'
           # print(nome_arquivo)
            if nome_arquivo.exists():
                nome_arquivo.unlink()  # apagar

        os.rename('relatoriocalculospdf.pdf', nome_arquivo)

        messages.success(request, ('Email sent successfully.'))
        return redirect('index')


@login_required(redirect_field_name='redirect_to')
def geradorPDFgeral(request, idb, ma):

    # Filtrando com dois parâmetros
    context = Condominio.objects.raw('''
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
            where m.id_bloco = %s and cal.mesano = %s 
            group by b.id_condominio, cd.nome , m.id_bloco,b.nome,cal.mesano,
                m.apto_sala,cad.nome
        ''', [idb, ma]
    )

    for lista in context:
        GerarPDF.get(None, request, ma=lista.mesano,
                     id_morador=lista.id_morador, idb=lista.id_bloco)

    # url = reverse('relatorio_calculos_pdf')
    return redirect('index')


@login_required(redirect_field_name='redirect_to')
def enviaremail(request, idb, ma):

    # Filtrando com dois parâmetros
    context = Condominio.objects.raw('''
          select distinct b.id_condominio, cd.nome nome_condominio, m.id_bloco,
                b.nome nome_bloco, 
                concat(left(cal.mesano,2),'/',right(cal.mesano,4)) as mes_ano,
                cal.mesano,
                m.apto_sala,
                cad.nome morador,m.id_morador, cad.email,
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
            where m.id_bloco = %s and cal.mesano = %s 
            group by b.id_condominio, cd.nome , m.id_bloco,b.nome,cal.mesano,
                m.apto_sala,cad.nome, cad.email
        ''', [idb, ma]
    )

    for lista in context:
       # print(lista.mesano, lista.email, lista.apto_sala)

        sendemail(request, ma=lista.mesano,
                  email=lista.email, apto=lista.apto_sala)

    # url = reverse('relatorio_calculos_pdf')
    return redirect('index')


def qrcode(request, valor, id_condominio):

    # Filtrando com dois parâmetros
    context = Condominio.objects.raw('''
            select id_condominio, cidade, responsavel_pix,chave_pix,txtid_pix
            from condominio
            where id_condominio = %s
        ''', [id_condominio]
    )
    for lista in context:
        payload = Payload(nome=lista.responsavel_pix, chavepix=lista.chave_pix,
                          valor=f'{valor}', cidade=lista.cidade, txtId=lista.txtid_pix)
        # pix_ = payload.gerarPayload()
        payload.gerarPayload()
        # print(pix_)
    return payload
