# from django.views.generic.list import ListView
from django.views.generic import TemplateView
# from django.views.generic.detail import deltail
from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.views.generic import View
from . models import Leituras, Calculos
from condominio.models import Morador
from django.db import connection
# from django.db.models import
from io import BytesIO
from django.http import FileResponse


from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from utils import utils
from PIL import Image
from reportlab.lib.utils import ImageReader
from django.urls import reverse
from django.db.models import Q
from movimentacao.forms import LeiturasForm


def lancar_leituras(request, idb, ma):

    registros = Morador.objects.filter(id_bloco=idb)
    submitted = False
    if request.method == 'POST':
        for registro in registros:
            prefixo = f'registro-{registro.id_morador}'
            form = LeiturasForm(
                request.POST, prefix=prefixo, instance=registro)
            if form.is_valid():
                form.save()
        return redirect('/listaconblomov/'+str(idb))
    else:
        form = LeiturasForm
        if submitted in request.GET:
            submitted = True

    # form = LeiturasForm()
    context = {
        'formulario':  Leituras.objects.raw('''
         select  max(id_leituras) id_leituras, max(l.mesano), m.apto_sala, cad.nome morador,  max(l.leitura_final) leitura_inicial, 0 leitura_final, valor_m3,
         dt_leitura,id_contas,
            case when ''' + str(ma[0:2]) + ''' <=9 then concat('0',''' + str(ma[0:2]) + ''','/',''' + str(ma[2:6]) + ''') else 
            concat(''' + str(ma[0:2]) + ''','/',''' + str(ma[2:6]) + ''')  end
              mes_ano,
            ''' + str(ma) + ''' mesano

            from morador m
            join cadastro cad on
			cad.id_cadastro = case when responsavel='I' then id_inquilino else id_proprietario end
            left join leituras l on
            m.id_morador = l.id_morador 
            left join contas ct on
            ct.id_conta = l.id_contas 
            where m.id_bloco =   ''' + str(idb) + '''
            group by  m.apto_sala, cad.nome 
            order by apto_sala
        '''),
        'form': form,
        'submitted': submitted
    }
    return render(request, "lancar_leituras.html", context)


class RelatorioCalculosPDF(View):

    def get(self, request,  *args, **kwargs):
        # Cria um objeto HttpResponse com o tipo de conteúdo PDF
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="relatoriocalculospdf.pdf"'

        # Cria o objeto canvas com o objeto HttpResponse
        p = canvas.Canvas(response)

        # Define a fonte e o tamanho da fonte
        p.setFont('Helvetica-Bold', 14)
        # Adiciona o texto ao cabeçalho

        p.drawString(
            180, 765, 'Relatório da Movimentação de contas Mês Ano: 02/2023')
        p.drawString(
            180, 765, '')
        # Define a cor do texto do cabeçalho
       # p.setFont('Helvetica', 14)

        # Define a cor de fundo do cabeçalho
        # cinza claro, ajuste os valores para a cor desejada
        # p.setFillColorRGB(0.5, 0.5, 0.5)
        # Desenha o cabeçalho com fundo colorido
        # p.rect(0, 750, 612, 50, fill=True)

        # Executa a consulta SQL bruta e itera sobre os resultados
        mesano_pk = ''' + str(ma) + '''
        with connection.cursor() as cursor:
            cursor.execute('''select cal.mesano, m.apto_sala, cad.nome morador,
                c.nome conta,
                m.foto,
                ROUND(valor,2) valor
                from calculos cal
                join contas c on
                c.id_conta = cal.id_contas
                join morador m on
                m.id_morador = cal.id_morador
                join cadastro cad on
                cad.id_cadastro = case when responsavel='I' then id_inquilino else id_proprietario end
                where cal.mesano = ''' + str(mesano_pk) + ''' order by mesano,m.apto_sala,id_contas'''
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
                mesano, apto_sala, morador, conta, foto, valor = row
                if apto_sala != apto_sala_anterior:
                    # Adiciona um subtotal para a categoria anterior
                    if apto_sala_anterior:
                        subtotal = subtotais[apto_sala_anterior]
                        p.setFont('Helvetica-Bold', 14)
                        p.drawString(
                            410, y, f'Subtotal...............: {subtotal:.2f}')
                        y -= 20
                    # Adiciona o cabeçalho da categoria
                    p.drawString(
                        50, y, f'Apto/Sala: {apto_sala} - {morador} ')
                    p.drawString(350, y, 'Conta')
                    p.drawString(550, y, 'Valor')
                    y -= 20
                    p.setFont('Helvetica', 14)
                    apto_sala_anterior = apto_sala
                    morador_anterior = morador
                if linha % 25 == 0 and linha != 0:
                    p.setFont('Helvetica-Bold', 14)
                    p.drawString(
                        180, 765, 'Relatório da Movimentação de contas Mês Ano: 02/2023')
                    p.setFont('Helvetica', 14)
                    # Define a cor do texto do cabeçalho
                    # Adiciona uma nova página depois de cada quatro linhas
                    p.showPage()
                    p.setFont('Helvetica', 14)
                    # if y < margem:
                    #   print(y)
                    y = 750
                if linha % 25 == 0:
                    # Desenha o cabeçalho com fundo colorido
                    p.setFont('Helvetica-Bold', 14)
                    p.drawString(
                        180, 765, 'Relatório da Movimentação de contas Mês Ano: 02/2023')
                    p.setFont('Helvetica', 14)
                    # Adiciona um cabeçalho a cada quatro linhas
                    # p.drawString(50, y,  'Mes Ano')
                    # p.drawString(100, y, 'Apto/Sala')
                    # p.drawString(150, y, 'Morador')
                    # p.drawString(350, y, 'Conta')
                    # p.drawString(500, y, 'Valor')
                    y -= 20
                # Adiciona os dados ao PDF
                # p.drawString(50, y, str(mesano))
                # p.drawString(100, y, str(apto_sala))
                # p.drawString(150, y, str(morador))
                p.drawString(350, y, str(conta))
                p.drawString(550, y, f'{utils.formata_valor(valor)}')
                y -= 20
                # Atualiza os subtotais e total geral
                if apto_sala not in subtotais:
                    subtotais[apto_sala] = 0
                subtotais[apto_sala] += valor
                total_geral += valor
                linha += 1

            # Adiciona o subtotal final
            subtotal = subtotais[apto_sala_anterior]
            p.setFont('Helvetica-Bold', 14)
            p.drawString(
                410, y, f'Subtotal.............: {utils.formata_valor(subtotal)}')
            y -= 20

            # Adiciona o total geral
            p.drawString(
                # 310, y, f'Total geral..........: {utils.formata_valor(total_geral)}')
                410, y, f'Total geral..........: {utils.formata_valor(total_geral)}')
            p.setFont('Helvetica', 14)
 # f'{val:.2f}'.replace('.', ',')
        # Finaliza o PDF e retorna o objeto HttpResponse
        p.showPage()
        p.save()
        return response


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
                ROUND(((leitura_final - leitura_inicial) * valor_m3),2) Valor,\
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
        # url = reverse('relatorio_calculos_pdf')
        return context


class Busca(ListaCalculo):
    def get_queryset(self, *args, **kwargs):
        termo = self.request.GET.get('termo') or self.request.session['termo']
        qs = super().get_queryset(*args, **kwargs)

        if not termo:
            return qs

        self.request.session['termo'] = termo

        qs = qs.filter(
            Q(apto_sala__icontains=termo) |
            Q(morador__icontains=termo)
        )

        self.request.session.save()
        return qs
