# from django.views.generic.list import ListView
from django.views.generic import TemplateView
# from django.views.generic.detail import deltail
# from django.shortcuts import render, redirect, reverse
# from django.http import HttpResponse
from django.contrib import messages
# from django.views import View
from . models import Leituras, Calculos
from django.db import connection
# from django.db.models import
import io
from django.http import FileResponse
from django.views.generic import View

from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter


class RelatorioCalculos(View):

    def get(sel, request, *args, **kwargs):
        # cria um arquivo para receber os dados e gerar o PDF
        buffer = io.BytesIO()

        # cria o arquivo PDF
        pdf = canvas.Canvas(buffer, pagesize=letter, bottomup=0)
        # cria o texto de objetos
        textob = pdf.beginText()
        textob.setTextOrigin(inch, inch)
        textob.setFont("Helvetica", 14)

        # leturas dos dados na tabela da query
        relatorios = Calculos.objects.raw("\
                select id_calculos, \
                concat(left(cal.mesano,2),'/',right(cal.mesano,4)) as mesano,\
                m.apto_sala, cad.nome morador, \
                c.nome conta,\
                ROUND(valor,2) valor\
                from calculos cal\
                join contas c on\
                c.id_conta = cal.id_contas\
                join morador m on\
                m.id_morador = cal.id_morador\
                join cadastro cad on\
                cad.id_cadastro = case when responsavel='I' then id_inquilino else id_proprietario end\
                where cal.mesano = 022023 and cal.id_morador = 1\
         ")
       # relatorios = Calculos.objects.all()
        # lines = []

        # for relatorio in relatorios:
        #     lines.append(str(relatorio.id_morador))
        #     lines.append(str(relatorio.id_contas))
        #     lines.append(str(relatorio.valor))
        #     lines.append(str(relatorio.mesano))
        #     lines.append(" ")

        # inserir dados no PRDF LOOP
        for relatorio in relatorios:
            # print(relatorio)
            textob.textLine(str(relatorio.mesano))
            textob.textLine(str(relatorio.apto_sala))
        pdf.drawText(textob)

        # quando acabamos de inserir no dpf
        pdf.showPage()
        pdf.save()

        # fim, retorna o buffer para o inicio do arquivo
        buffer.seek(0)

        return FileResponse(buffer, as_attachment=True, filename='relcal.pdf')


class ListaLeitura(TemplateView):
    template_name = 'movimentacao/lista_leitura.html'
    paginate_by = 2

    def get_context_data(self, **kwargs):
        context = super(ListaLeitura, self).get_context_data(**kwargs)
        context = {
            'leituras':  Leituras.objects.raw("\
            select concat(left(mesano,2),'/',right(mesano,4)) as mesano, \
                id_leituras as id_leituras, \
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


class ListaCalculo(TemplateView):
    template_name = 'movimentacao/lista_calculo.html'
    paginate_by = 2

    def get_context_data(self, **kwargs):
        context = super(ListaCalculo, self).get_context_data(**kwargs)
        context = {
            'calculos':  Calculos.objects.raw("\
            select id_calculos ,\
                concat(left(mesano,2),'/',right(mesano,4)) as mesano,\
                m.apto_sala,\
                cad.nome morador,\
                count(*) qde_contas,\
                ROUND(sum(valor), 2) valor \
            from calculos cal\
                join contas c on\
                c.id_conta=cal.id_contas\
                join morador m on\
                m.id_morador=cal.id_morador\
                join cadastro cad on\
                cad.id_cadastro=case when responsavel='I' \
                then id_inquilino else id_proprietario end\
            group by cal.mesano, m.apto_sala, cad.nome  WITH ROLLUP \
         ")
        }
        return context
