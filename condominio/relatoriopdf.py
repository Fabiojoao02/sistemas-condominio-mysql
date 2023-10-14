import os
import time
import urllib.parse
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
from reportlab.lib.colors import red, black, blue, gray, green, yellowgreen, orange, white
from django.contrib import messages
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.platypus import Table, TableStyle, Image
from pathlib import Path

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
from io import BytesIO
from django.conf import settings
from django.contrib.auth.models import User, Group
from reportlab.graphics.charts.linecharts import HorizontalLineChart
from reportlab.graphics.widgets.markers import makeMarker


class GeraRelatorioPDF(View):

    def get(self, request, ma, idb):

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
        response['Content-Disposition'] = 'attachment; filename="relatoriocalculospdf.pdf"'

        # Cria o objeto canvas com o objeto HttpResponse
        # case usar o comando acima abre um pop para definir o local para salvar
        p = canvas.Canvas(response)
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
            cursor.execute('''
                  select b.id_condominio, cond.nome condominio, m.id_bloco, cond.foto, b.nome nome_bloco,
                        concat(left(cal.mesano,2),'/',right(cal.mesano,4)) as mes_ano,
                        cal.mesano,
                        m.apto_sala, m.id_morador,
                        cad.nome morador,
                        count(*) qde_contas,
                        ROUND(sum(valor), 2) valor 
                     from calculos cal
                        join morador m on
                           m.id_morador=cal.id_morador
                        join cadastro cad on
                           cad.id_cadastro=case when responsavel='I' 
                                 then id_inquilino else id_proprietario end
                        join bloco b on
                           b.id_bloco = m.id_bloco
                        join condominio cond on
                        cond.id_condominio = b.id_condominio                               
                     where m.id_bloco = %s and cal.mesano = %s
                     group by b.id_condominio,m.id_bloco,mesano,m.apto_sala,cad.nome,m.id_morador,cond.foto,cond.foto , b.nome,cond.nome  
                     order by cal.mesano, m.id_bloco,m.apto_sala
                     ''', [idb, ma]
                           )
            rows = cursor.fetchall()
            y = 750
            linha = 0
            subtotais = {}
            # margem = 50
            total_geral = 0
            id_bloco_anterior = None
            mesano_anterior = None
            for row in rows:
                id_condominio, condominio, id_bloco, foto, nome_bloco, mes_ano, mesano, apto_sala, id_morador, morador, qde_contas, valor = row
                image_filename = foto
                # image_path = os.path.join('condominio_imagens', image_filename)
                image_full_path = os.path.join(
                    settings.MEDIA_ROOT, image_filename)

                image_full_path = image_full_path.replace('\\', '/')

                # print(image_data)
                with open(image_full_path, 'rb') as f:
                    image_data = f.read()

                image = ImageReader(BytesIO(image_data))

                p.drawImage(image,
                            x=10, y=710, width=130, height=130)
                if mesano != mesano_anterior:
                    # Adiciona imagem do condominio
                    # Adiciona um subtotal para a categoria anterior
                    if mesano_anterior:
                        subtotal = subtotais[mesano_anterior]
                        p.setFont('Helvetica-Bold', 14)
                        p.drawAlignedString(
                            210, y, f'Subtotal...............: {subtotal:.2f}')
                        y -= 20
                    # Adiciona o cabeçalho da categoria
                    # p.drawString(100, 100, '\n\n')
                    p.setFillColor(blue)
                    p.drawString(
                        150, 800, f'{condominio} - {nome_bloco} ')
                    p.setFillColor(black)
                    y -= 20
                    p.setFont('Helvetica', 14)
                    id_bloco_anterior = id_bloco
                    mesano_anterior = mesano
                if linha % 25 == 0 and linha != 0:
                    p.setFont('Helvetica-Bold', 14)
                    p.drawString(
                        150, 765, 'Relatório gerencial das contas Mês Ano: '+mes_ano)
                    # p.drawString(100, 100, '\n\n')
                    p.setFont('Helvetica', 14)
                    # Define a cor do texto do cabeçalho
                    # Adiciona uma nova página depois de cada quatro linhas
                    p.drawString(150, y, 'Apto/Sala - Morador')
                    p.drawAlignedString(500, y, 'Valor')
                    p.showPage()
                    p.setFont('Helvetica', 14)
                    y = 750
                if linha % 25 == 0:
                    # Desenha o cabeçalho com fundo colorido
                    # p.drawString(100, 100, '\n\n')
                    p.setFont('Helvetica-Bold', 14)
                    p.drawString(
                        150, 765, 'Relatório gerencial das contas Mês Ano: '+mes_ano)
                    # p.drawString(100, 100, '\n\n')
#                    y -= 20
                    p.drawString(150, y, 'Apto/Sala - Morador')
                    p.drawAlignedString(500, y, 'Valor')
                    p.setFont('Helvetica', 14)
                    y -= 20
                # Adiciona os dados ao PDF
                p.drawString(
                    150, y, f'{apto_sala} - {morador} ')

                # rows.setStyle(style)  # Aplica o estilo à tabela
                p.drawAlignedString(
                    500, y, f'{utils.formata_valor(valor)}')
                y -= 20
                # Atualiza os subtotais e total geral
                if mesano_anterior not in subtotais:
                    subtotais[mesano] = 0
                subtotais[mesano] += valor
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

        # graficos movimento condomino
        # Executa a consulta SQL bruta e itera sobre os resultados
        separador = '%'
        with connection.cursor() as cursor:
            cursor.execute(
                """
                  SELECT distinct 
                     concat(cad.nome,'-',
                     CAST(ROUND((SELECT SUM(c1.valor) 
                        FROM calculos c1
                        WHERE c1.id_morador = cal.id_morador 
                           AND c1.mesano = cal.mesano 
                           AND c1.id_bloco = cal.id_bloco
                     ) / 
                     (SELECT SUM(c2.valor) 
                        FROM calculos c2
                        WHERE c2.mesano = cal.mesano  
                           AND c2.id_bloco = cal.id_bloco
                     )*100,2) as char),%s) AS percentual,
                     ROUND((SELECT SUM(c1.valor) 
                        FROM calculos c1
                        WHERE c1.id_morador = cal.id_morador 
                           AND c1.mesano = cal.mesano 
                           AND c1.id_bloco = cal.id_bloco
                     ),2) valor                     
                  FROM calculos cal
                  JOIN morador c ON c.id_morador = cal.id_morador
                  JOIN cadastro cad ON 
                     (c.responsavel = 'I' AND cad.id_cadastro = c.id_inquilino) OR
                     (c.responsavel = 'P' AND cad.id_cadastro = c.id_proprietario)
                  WHERE cal.mesano = %s
                  AND cal.id_bloco = %s
            """,
                # [ma, id_morador]
                [([separador]), ma, idb]

            )
            dados = cursor.fetchall()
            # *********************************Grafica de Barras
            # Cria o gráfico de barras verticais
            y = 700
            # Criando o objeto Drawing para conter o gráfico
            # Criando a lista de labels e valores a partir dos dados da query
            labels = [label for label, _ in dados]
            valores = [valor for _, valor in dados]

            # Criando o objeto Drawing para conter o gráfico
            d = Drawing(100, 500)

            # Configurando o gráfico de barras verticais
            chart = VerticalBarChart()
            chart.x = 50
            chart.y = 30
            chart.height = 200
            chart.width = 400
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
            # p.showPage()

            # ****************Leitura do Gás
        # Executa a consulta SQL bruta e itera sobre os resultados
        with connection.cursor() as cursor:
            cursor.execute('''
                    select c.nome conta,
                            concat(left(lei.mesano,2),'/',right(lei.mesano,4)) as mes_ano,
                            lei.mesano,
                            m.apto_sala, m.id_morador,cad.nome morador,
                            cast(lei.dt_leitura as date) as dt_leitura, valor_m3,
                            leitura_final, leitura_inicial, 
                            round((leitura_final - leitura_inicial),3)  consumo_m3,
                            round(((leitura_final - leitura_inicial) * valor_m3),2) vl_consumo
                        from leituras lei
                            join contas c on
                                c.id_conta=lei.id_contas
                            join morador m on
                                m.id_morador=lei.id_morador
                            join cadastro cad on
                                cad.id_cadastro=case when responsavel='I' 
                                    then id_inquilino else id_proprietario end
                            join bloco b on
                                b.id_bloco = m.id_bloco
                        where (lei.leitura_final - lei.leitura_inicial) > 0 and m.id_bloco = %s and lei.mesano = %s
                        group by b.id_condominio,m.id_bloco,lei.mesano,m.apto_sala,cad.nome,m.id_morador 
                        order by lei.mesano, m.id_bloco,m.apto_sala       
                     ''', [idb, ma]
                           )
            rowsl = cursor.fetchall()
            if len(rowsl) > 0:
                p.showPage()
                y = 750
                linha = 0
                subtotais = {}
                # margem = 50
                total_geral_valor = 0
                total_geral_consumo = 0
                subtotal = 0
                conta_anterior = None
                for row in rowsl:
                    conta, mes_ano, mesano, apto_sala, id_morador, morador, dt_leitura, valor_m3, leitura_final, leitura_inicial, consumo_m3,  vl_consumo = row
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
                            180, 765, f'leitura de {conta} mês {mes_ano}')
                        p.setFont('Helvetica', 14)
                        # Define a cor do texto do cabeçalho
                        # Adiciona uma nova página depois de cada quatro linhas
                        # dt_leitura, valor_m3, leitura_final, leitura_inicial, consumo_m3, vl_consumo
                        p.setFont('Helvetica-Bold', 8)
                        p.drawString(10, y, 'Apto/Sala')
                        p.drawString(60, y, 'Morador')
                        p.drawString(160, y, 'dt_leitura')
                        p.drawString(240, y, 'valor_m3')
                        p.drawString(300, y, 'leitura_inicial')
                        p.drawString(370, y, 'leitura_final')
                        p.drawString(450, y, 'consumo_m3')
                        p.drawString(525, y, 'vl_consumo')
                        p.showPage()
                        p.setFont('Helvetica', 14)
                        y = 750
                    if linha % 25 == 0:
                        # Desenha o cabeçalho com fundo colorido
                        p.setFont('Helvetica-Bold', 14)
                        p.drawString(
                            180, 765, f'leitura de {conta} mês {mes_ano}')
                        p.setFont('Helvetica-Bold', 8)
                        p.drawString(10, y, 'Apto/Sala')
                        p.drawString(60, y, 'Morador')
                        p.drawString(180, y, 'Data leitura')
                        p.drawString(240, y, 'Valor m3')
                        p.drawString(300, y, 'Leitura Inicial')
                        p.drawString(380, y, 'Leitura Final')
                        p.drawString(450, y, 'Consumo m3')
                        p.drawString(530, y, 'Valor Consumo')
                    #  p.showPage()
                        y -= 20
                    # Adiciona os dados ao PDF
                    p.setFont('Helvetica-Bold', 8)
                    p.drawString(15, y, str(apto_sala))
                    p.drawString(60, y, str(morador))
                    p.drawString(180, y, str(dt_leitura))
                    p.drawAlignedString(
                        268, y, f'{utils.formata_valor(valor_m3)}')
                    p.drawAlignedString(330, y, str(leitura_inicial))
                    p.drawAlignedString(410, y, str(leitura_final))
                    p.drawAlignedString(
                        500, y, f'{utils.formata_valorm3(consumo_m3)}')
                    p.drawRightString(
                        575, y, f'{utils.formata_valor(vl_consumo)}')

                    y -= 20
                    # Atualiza os subtotais e total geral
                    if conta not in subtotais:
                        subtotais[conta] = 0
                    # subtotais[conta] += vl_consumo
                    total_geral_valor += vl_consumo
                    total_geral_consumo += consumo_m3
                    linha += 1

            # Adiciona o total geral
            p.setFont('Helvetica-Bold', 14)
            # 310, y, f'Total geral..........: {utils.formata_valor(total_geral)}')
            p.drawString(
                250, y, f'Total geral')
            p.drawAlignedString(
                500, y, f'{utils.formata_valor(total_geral_consumo )}'
            )
            p.drawAlignedString(
                580, y, f'{utils.formata_valor(total_geral_valor )}'
            )
            p.setFont('Helvetica', 14)

        # graficos movimento condomino
        # Executa a consulta SQL bruta e itera sobre os resultados
        separador = '%'
        with connection.cursor() as cursor:
            cursor.execute(
                """
                 SELECT distinct 
                     concat(cad.nome,'-',
                     CAST(ROUND((SELECT SUM((c1.leitura_final - c1.leitura_inicial)) 
                        FROM leituras c1
                        WHERE c1.id_morador = cal.id_morador 
                           AND c1.mesano = cal.mesano 
                           AND c1.id_bloco = cal.id_bloco
                     ) / 
                     (SELECT SUM((c2.leitura_final - c2.leitura_inicial)) 
                        FROM leituras c2
                        WHERE c2.mesano = cal.mesano  
                           AND c2.id_bloco = cal.id_bloco
                     )*100,2) as char),%s) AS percentual,
                     ROUND((SELECT SUM((c1.leitura_final - c1.leitura_inicial)) 
                        FROM leituras c1
                        WHERE c1.id_morador = cal.id_morador 
                           AND c1.mesano = cal.mesano 
                           AND c1.id_bloco = cal.id_bloco
                     ),3) valor                     
                  FROM leituras cal
                  JOIN morador c ON c.id_morador = cal.id_morador
                  JOIN cadastro cad ON 
                     (c.responsavel = 'I' AND cad.id_cadastro = c.id_inquilino) OR
                     (c.responsavel = 'P' AND cad.id_cadastro = c.id_proprietario)
                  WHERE (cal.leitura_final - cal.leitura_inicial) > 0
                  AND cal.mesano = %s
                  AND cal.id_bloco = %s
                """,
                # [ma, id_morador]
                [([separador]), ma, idb]

            )
            dados = cursor.fetchall()
            # *********************************Grafica de Barras
            # Cria o gráfico de barras verticais
            y = 700
            # Criando o objeto Drawing para conter o gráfico
            # Criando a lista de labels e valores a partir dos dados da query
            labels = [label for label, _ in dados]
            valores = [valor for _, valor in dados]

            # Criando o objeto Drawing para conter o gráfico
            d = Drawing(100, 500)

            # Configurando o gráfico de barras verticais
            chart = VerticalBarChart()
            chart.x = 50
            chart.y = 30
            chart.height = 200
            chart.width = 400
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
            # p.showPage()

# Inicio grafico de linhas de tempo do gas
        # graficos movimento condomino
        # Executa a consulta SQL bruta e itera sobre os resultados

           # ****************Leitura do Gás
        # Executa a consulta SQL bruta e itera sobre os resultados
        with connection.cursor() as cursor:
            cursor.execute('''
                    select volume_m3, 
                           cast(max(dt_troca) as date) dt_troca,
                    max(DATEDIFF(dt_leitura, dt_troca)) dias,
                    concat(left(max(l.mesano),2),'/',right(max(l.mesano),4)) as mes_ano,
                    round((select sum(leitura_final)  - sum(leitura_inicial) 
                            from leituras l1
                            join bloco b1 on
                            b1.id_bloco = l1.id_bloco
                            join controlegas gas1 on
                            gas1.id_condominio = b1.id_condominio
                            where DATEDIFF(dt_leitura, dt_troca) > 0 and l1.id_bloco = l.id_bloco
                    ),3) acumuado_m3,
                    round(volume_m3 -(select sum(leitura_final)  - sum(leitura_inicial) 
                            from leituras l1
                            join bloco b1 on
                            b1.id_bloco = l1.id_bloco
                            join controlegas gas1 on
                            gas1.id_condominio = b1.id_condominio
                            where DATEDIFF(dt_leitura, dt_troca) > 0 and l1.id_bloco = l.id_bloco
                    ) ,3) 
                    saldo,
                    round(100-((select sum(leitura_final)  - sum(leitura_inicial) 
                            from leituras l1
                            join bloco b1 on
                            b1.id_bloco = l1.id_bloco
                            join controlegas gas1 on
                            gas1.id_condominio = b1.id_condominio
                            where DATEDIFF(dt_leitura, dt_troca) > 0 and l1.id_bloco = l.id_bloco
                    )/volume_m3)*100 ,1) as percentual,
                    round((max(DATEDIFF(dt_leitura, dt_troca)) * volume_m3) /
                    (select sum(leitura_final)  - sum(leitura_inicial) 
                            from leituras l1
                            join bloco b1 on
                            b1.id_bloco = l1.id_bloco
                            join controlegas gas1 on
                            gas1.id_condominio = b1.id_condominio
                            where DATEDIFF(dt_leitura, dt_troca) > 0 and l1.id_bloco = l.id_bloco
                    )-max(DATEDIFF(dt_leitura, dt_troca)),0)  as estimativa_falta_em_dias
                    from leituras l
                    join bloco b on
                    b.id_bloco = l.id_bloco
                    join controlegas gas on
                    gas.id_condominio = b.id_condominio
                    where l.id_bloco = %s
                    and DATEDIFF(dt_leitura, dt_troca) >0

            ''', [idb]
            )
            rowsg = cursor.fetchall()
            if len(rowsg) > 0:
                p.showPage()
                y = 200
                linha = 0
                subtotais = {}
                # margem = 50
                total_geral_valor = 0
                total_geral_consumo = 0
                subtotal = 0
                conta_anterior = None
                for row in rowsg:
                    volume_m3, dt_troca, dias, mes_ano,  acumuado_m3, saldo, percentual, estimativa_falta_em_dias = row

                    # Converter dt_troca para o formato "d/m/Y"
                    dt_troca_formatada = dt_troca.strftime("%d/%m/%Y")
                    estimativa_falta_em_dias = int(estimativa_falta_em_dias)
                    p.setFont('Helvetica-Bold', 14)

                    p.setFillColor(blue)
                    p.drawString(
                        150, 800, 'Controle cilindro gás')
                    p.setFillColor(black)

                    # p.setFont('Helvetica-Bold', 12)
                    texto = f'''
                    Cilindro P45 contendo 20kg, equivalente volume cúbico {utils.formata_valorm3(volume_m3)}m3 
                    troca do cilindro efetuada dia {dt_troca_formatada} no momento temos {dias} dias,
                    um total acumulado de {utils.formata_valorm3(acumuado_m3)}m3 com um saldo de {utils.formata_valorm3(saldo)}m3, 
                    mês e ano atual {mes_ano}.
                    '''
                    linhas = texto.split('\n')
                    for i, linha in enumerate(linhas):
                        p.drawString(10, 780 - i*15, linha)

                    # percentual = 50

                    if percentual < 25:
                        p.setFont('Helvetica-Bold', 12)
                        p.setFillColor(red)
                    elif percentual >= 25 and percentual <= 49:
                        p.setFont('Helvetica-Bold', 12)
                        p.setFillColor(orange)
                    else:
                        p.setFont('Helvetica-Bold', 12)
                        p.setFillColor(green)

                    p.drawString(
                        150, 695, f'Capacidade até o momento no cilindro {percentual}% de gás.')
                    p.drawString(
                        150, 680, f'Estimativa em dias do cilindro {estimativa_falta_em_dias} dias.')
                    p.setFillColor(black)

        # *INICIO*************query grafico guage
        with connection.cursor() as cursor:
            cursor.execute(
                """
                    select  distinct 
                    round(((select sum(leitura_final)  - sum(leitura_inicial) 
                            from leituras l1
                            join bloco b1 on
                            b1.id_bloco = l1.id_bloco
                            join controlegas gas1 on
                            gas1.id_condominio = b1.id_condominio
                            where DATEDIFF(dt_leitura, dt_troca) > 0 and l1.id_bloco = l.id_bloco
                    )/volume_m3)*100 ,2) as percentual
                    from leituras l
                    join bloco b on
                    b.id_bloco = l.id_bloco
                    join controlegas gas on
                    gas.id_condominio = b.id_condominio
                    where l.id_bloco = %s
                    and DATEDIFF(dt_leitura, dt_troca) >0
                """,
                [idb]
            )
            dados = cursor.fetchall()

            percentual = dados[0][0]

            p.setFillColor(black)
            p.drawString(150, 632, 'Mapa do cilindro')
            # Chama a função para desenhar o medidor
            utils.draw_gauge(p, percentual)
            # d.add(chart)
            # renderPDF.draw(d, p, 100, y)

        # *FIM*************query grafico guage

        # **************query grafico de barras
        with connection.cursor() as cursor:
            cursor.execute(
                """
                    select concat(left(l.mesano,2),'/',right(l.mesano,4)) as mes_ano,
                    round(sum(leitura_final)  - sum(leitura_inicial),3)  total
                    from leituras l
                    join bloco b on
                    b.id_bloco = l.id_bloco
                    join controlegas gas on
                    gas.id_condominio = b.id_condominio
                    where l.id_bloco = %s
                    and DATEDIFF(dt_leitura, dt_troca) > 0
                    group by cast(dt_leitura as date),l.mesano,volume_m3
                """,
                [idb]

            )
            dados = cursor.fetchall()
            # *********************************Grafica de Barras
            # Cria o gráfico de barras verticais
            y = 200
            # Criando o objeto Drawing para conter o gráfico
            # Criando a lista de labels e valores a partir dos dados da query
            labels = [label for label, _ in dados]
            valores = [valor for _, valor in dados]

            # Criando o objeto Drawing para conter o gráfico
            d = Drawing(100, 500)

            # Configurando o gráfico de barras verticais
           # Configurando o gráfico de barras verticais
            chart = HorizontalLineChart()
            chart.x = 50
            chart.y = 60
            chart.height = 200
            chart.width = 350
            chart.data = [valores]

            chart.joinedLines = 1
            catNames = labels
            chart.categoryAxis.categoryNames = catNames
            chart.categoryAxis.labels.boxAnchor = 'n'
            chart.valueAxis.valueMin = 0
            chart.valueAxis.valueMax = 45
            chart.valueAxis.valueStep = 5
            chart.lines[0].strokeWidth = 2
            chart.lines[1].strokeWidth = 1.5

            # # Adicionando os valores sobre os rótulos de barra
            for i, data in enumerate(chart.data):
                for j, value in enumerate(data):
                    x = chart.x + j * (chart.width / len(data)) + \
                        (chart.width / len(data)) / 2
                    y = chart.y + chart.height + 10
                    # label = String(x, y, str(value))
                    label = String(x, y, f'{utils.formata_valorm3(value)}')
#                    label.fontName = 'Helvetica'
                    label.fontSize = 10
                    label.textAnchor = 'middle'
                    d.add(label)

            # Calcular os valores acumulados
            acumulado = [sum(valores[:i+1]) for i in range(len(valores))]

            # Adicionar os dados acumulados ao gráfico
            chart.data.append(acumulado)

            # Adicionar os valores acumulados sobre os rótulos de barra
            for i, data in enumerate(chart.data):
                for j, value in enumerate(data):
                    x = chart.x + j * (chart.width / len(data)) + \
                        (chart.width / len(data)) / 2
                    if i == 0:
                        y = chart.y + chart.height + 10
                    else:
                        y = chart.y + chart.height + 25  # Ajuste aqui para evitar sobreposição
                    label = String(x, y, f'{utils.formata_valorm3(value)}')
                    label.fontSize = 10
                    label.textAnchor = 'middle'
                    d.add(label)

        with connection.cursor() as cursor:
            cursor.execute(
                """
                    select distinct volume_m3,
                    round(volume_m3 -(select sum(leitura_final)  - sum(leitura_inicial) 
                            from leituras l1
                            join bloco b1 on
                            b1.id_bloco = l1.id_bloco
                            join controlegas gas1 on
                            gas1.id_condominio = b1.id_condominio
                            where DATEDIFF(dt_leitura, dt_troca) > 0 and l1.id_bloco = l.id_bloco
                    ) ,3) saldo
                    from leituras l
                    join bloco b on
                    b.id_bloco = l.id_bloco
                    join controlegas gas on
                    gas.id_condominio = b.id_condominio
                    where l.id_bloco = %s
                    and DATEDIFF(dt_leitura, dt_troca) > 0
                """,
                [idb]

            )
            dados = cursor.fetchall()
            # Certifique-se de que a consulta retornou algum dado
            if dados:
                # Acesso ao primeiro valor da primeira linha
                meta_valor = dados[0][0]
                meta_valor_plotar = dados[0][0]/2
                saldo = dados[0][1]
            else:
                # Trate o caso em que não há dados retornados pela consulta
                meta_valor = None
                saldo = None

                # Adicionar a linha da meta ao gráfico
            meta_y = chart.y + (chart.height *
                                (1 - (meta_valor / chart.valueAxis.valueMax)))
            # Ajustar a posição da meta para a escala desejada
            if chart.y <= meta_y <= chart.y + chart.height:
                d.add(Line(chart.x, meta_y, chart.x + chart.width,
                           meta_y, strokeWidth=1, strokeColor=colors.green))

                # Calcular a posição para o rótulo da meta
                label_x = chart.x  # + chart.width
                label_y = meta_y - 10
                # Adicionar um rótulo para indicar o valor da meta
                label = String(
                    label_x, label_y, f'Capacidade total m3: {meta_valor}', fontSize=10, fillColor=colors.black)
                d.add(label)
            # Adicionando o gráfico ao objeto Drawing
            d.add(chart)
            renderPDF.draw(d, p, 100, y)
        # fim grafico de linha no tempo do gas

        # Fim leitura do gas

            p.save()

            nome_arquivo = arquivo / f'{ma}_{idb}.pdf'
            print(nome_arquivo)
            if nome_arquivo.exists():
                nome_arquivo.unlink()  # apagar

        os.rename('relatoriocalculospdf.pdf', nome_arquivo)

        # Construa a nova URL com o novo parâmetro
        nova_url = f'/listaconblomov/{idb}/'

        messages.success(request, ('Email sent successfully.'))
        return redirect(nova_url)
