from django.db import models, connection
from django.db.models import Avg, Count, Min, Sum
from conta.models import Contas
from tipocalculo.models import TipoCalculo
from cadastro.models import Cadastro
from condominio.models import Morador
from django.utils.safestring import mark_safe
from utils import utils
from django.shortcuts import render


class Calculos(models.Model):
    id_calculos = models.AutoField(primary_key=True)
    id_morador = models.ForeignKey(
        Morador, models.DO_NOTHING, db_column='id_morador')


#    models.IntegerField()
    id_contas = models.ForeignKey(
        Contas, models.DO_NOTHING, db_column='id_contas', related_name='id_contas')
    valor = models.FloatField()
    publica = models.BooleanField(default=True)
    dt_lancamento = models.DateTimeField()
    mesano = models.CharField(max_length=6)

    def get_formatvalorCal(self):
        return f'{self.valor:.2f}'.replace('.', ',')
    get_formatvalorCal.short_description = 'Valor'

    def get_nome_moradorCal(self):
        return '%s' % (self.id_morador.id_inquilino).nome
    get_nome_moradorCal.short_description = 'Morador'

   # @property
    def get_apto_salaCal(self):
        return '%s' % (self.id_morador.apto_sala)
    get_apto_salaCal.short_description = 'Apto/sala'

    def get_contascalculo(self):
        return '%s' % (self.id_contas.nome)
    get_contascalculo.short_description = 'Contas'

    def get_formata_mesano_calculo(self):
        return utils.formata_mesano(self.mesano)
    get_formata_mesano_calculo.short_description = 'MES/ANO'

    def __str__(self) -> str:
        return self.mesano

    class Meta:
        managed = False
        db_table = 'calculos'
        verbose_name = 'Calculo'
        verbose_name_plural = 'Calculos'


class Leituras(models.Model):
    id_leituras = models.AutoField(primary_key=True)
    mesano = models.CharField(max_length=6, verbose_name='MES/ANO')
    id_morador = models.ForeignKey(
        Morador, models.DO_NOTHING, db_column='id_morador')
    id_contas = models.ForeignKey(
        Contas, models.DO_NOTHING, db_column='id_contas')
    dt_leitura = models.DateField()
    vl_gas_m3 = models.FloatField()
    leitura_inicial = models.FloatField()
    leitura_final = models.FloatField()

    # def dictfetchall(cursor):
    #     desc = cursor.description
    #     return [
    #         dict(zip([col[0] for col in desc], row))
    #         for row in cursor.fetchall()
    #     ]

    # def listaleitura(request):
    #     cursor = connection.cursor()
    #     cursor.execute("\
    #         select concat(left(mesano,2),'/',right(mesano,4)) as mesano \
    #             , id_leituras as id_leituras, \
    #             l.id_morador as id_morador, \
    #             cad.nome morador, c.nome as Conta, vl_gas_m3, \
    #             leitura_inicial, leitura_final, \
    #             ROUND((leitura_final - leitura_inicial),3) as Consumo_m3, \
    #             ROUND(((leitura_final - leitura_inicial) * vl_gas_m3),2) Valor,\
    #             cast(dt_leitura as date) dt_leitura \
    #         from leituras  l \
    #         join morador m on \
    #             m.id_morador = l.id_morador  \
    #         join cadastro cad on \
    #             cad.id_cadastro = id_inquilino \
    #         join contas c on \
    #             c.id_conta = l.id_contas \
    # ")
    #     model = dictfetchall(cursor)
    #     paginate_by = 2
    #     return render(request, 'movimentacao/lista_leitura.html', {'leituras': model})

    def get_formatvlgasm3(self):
        return f'{self.vl_gas_m3:.2f}'.replace('.', ',')
    get_formatvlgasm3.short_description = 'Vl gas m3'

    def get_contasleitura(self):
        return '%s' % (self.id_contas.nome)
    get_contasleitura.short_description = 'Contas'

    def get_nome_moradorLei(self):
        return '%s' % (self.id_morador.id_inquilino).nome
    get_nome_moradorLei.short_description = 'Morador'

   # @property
    def get_apto_salaLei(self):
        return '%s' % (self.id_morador.apto_sala)
    get_apto_salaLei.short_description = 'Apto/sala'

    def get_formata_mesano_leitura(self):
        return utils.formata_mesano(self.mesano)
    get_formata_mesano_leitura.short_description = 'MES/ANO'

   # def imprimir(self):
    #    return mark_safe("""<a href=\"leiturasmes/%s\" target="_blank"><img src=\"/static/images/b_print.png\"></a>""" % self.id_leituras)
    # return mark_safe("""<a href="{% url 'leiturasmes' leitura_id %}">\" target="_blank"><img src=\"/static/images/b_print.png\"></a>""")

    # calculo

    def __str__(self) -> str:
        return self.mesano

    class Meta:
        managed = False
        db_table = 'leituras'
        verbose_name = 'Leitura'
        verbose_name_plural = 'Leituras'


class Movimento(models.Model):
    id_movimento = models.AutoField(primary_key=True)
    mesano = models.CharField(max_length=6)
    id_contas = models.ForeignKey(
        Contas, models.DO_NOTHING, db_column='id_contas')
    valor = models.FloatField()
    id_tipo_calculo = models.ForeignKey(
        TipoCalculo, models.DO_NOTHING, db_column='id_tipo_calculo')
    dt_lancamento = models.DateTimeField()

    def get_contasmovimento(self):
        return '%s' % (self.id_contas.nome)
    get_contasmovimento.short_description = 'Contas'

    def get_tipo_calculomov(self):
        return '%s' % (self.id_tipo_calculo.descricao)
    get_tipo_calculomov.short_description = 'Tipo Conta'

    def get_formatValorMov(self):
        return f'{self.valor:.2f}'.replace('.', ',')
    get_formatValorMov.short_description = 'Valor'

    def get_formata_mesano_movimento(self):
        return utils.formata_mesano(self.mesano)
    get_formata_mesano_movimento.short_description = 'MES/ANO'

    def __str__(self) -> str:
        return self.mesano

    class Meta:
        managed = False
        db_table = 'movimento'
        unique_together = (('mesano', 'id_contas'),)
        verbose_name = 'Movimento'
        verbose_name_plural = 'Movimentos'

# class RawChangeList(ChangeList):
#     """
#     Extended Django ChangeList to be able show data from RawQueryset.
#     """
#     def get_count(self):
#         connection = connections[self.queryset.db]
#         with connection.cursor() as c:
#             if connection.vendor == 'microsoft':  # CTE in subquery is not working in SQL Server
#                 c.execute(self.queryset.raw_query)
#                 c.execute('SELECT @@ROWCOUNT')
#             else:
#                 query = 'SELECT COUNT(*) FROM ({query}) AS sq'
#                 c.execute(query.format(query=self.queryset.raw_query))

#             return c.fetchone()[0]

#     def get_queryset_slice(self):
#         connection = connections[self.queryset.db]
#         if connection.vendor == 'microsoft':
#             # SQL Server needs ordered query for slicing
#             if hasattr(self.queryset, 'ordered') and self.queryset.ordered:
#                 query = '{query}'
#             else:
#                 query = '{query} ORDER BY 1'
#             query += ' OFFSET {offset} ROWS FETCH NEXT {limit} ROWS ONLY'
#         else:
#             query = '{query} LIMIT {limit} OFFSET {offset}'

#         return self.queryset.model.objects.raw(
#             query.format(
#                 query=self.queryset.raw_query,
#                 offset=self.page_num * self.list_per_page,
#                 limit=(self.page_num + 1) * self.list_per_page - self.page_num * self.list_per_page,
#             )
#         )

#     def get_queryset(self, request):
#         """
#         Overriding to avoid applying filters in ChangeList because RawQueryset has not filter method.
#         So any filters has to be applied manually for now.
#         """
#         qs = self.root_queryset
#         if not hasattr(qs, 'count'):
#             qs.count = lambda: self.get_count()
#         return qs

#     def get_results(self, request):
#         if self.show_all:
#             qs = self.queryset
#         else:
#             qs = self.get_queryset_slice()

#         paginator = self.model_admin.get_paginator(request, self.queryset, self.list_per_page)

#         self.result_count = paginator.count
#         self.show_full_result_count = False
#         self.show_admin_actions = True
#         self.full_result_count = 0
#         self.result_list = list(qs)
#         self.can_show_all = True
#         self.multi_page = True
#         self.paginator = paginator
