from django.contrib import admin
# from . import models
from django.db.models import Sum
from .models import Leituras, Calculos, Movimento, Cadastro
from django.db import connection


@admin.register(Calculos)
class CalculosAdmin(admin.ModelAdmin):
    list_display = ('mesano', 'id_morador', 'valor')

    def get_queryset(self, request):
        with connection.cursor() as cursor:
            cursor.execute('''
            select cal.mesano, cal.id_morador,
             ROUND(sum(valor),2) valor
            from calculos cal
            join contas c on
            c.id_conta = cal.id_contas
            join morador m on
            m.id_morador = cal.id_morador
            join cadastro cad on
            cad.id_cadastro = case when responsavel='I' then id_inquilino else id_proprietario end
            group by cal.mesano, cal.id_morador
        ''')
        results = cursor.fetchall()
       # print([{'mesano': row[0], 'id_morador': row[1], 'valor': row[2]}
        #      for row in results])
        return [{'mesano': row[0], 'id_morador': row[1], 'valor': row[2]} for row in results]


@ admin.register(Leituras)
class LeiturasAdmin(admin.ModelAdmin):

    list_display = ['id_leituras', 'get_formata_mesano_leitura', 'get_apto_salaLei', 'get_nome_moradorLei', 'get_contasleitura',
                    'get_formatvalorm3', 'leitura_inicial', 'leitura_final', 'dt_leitura']
    list_per_page = 15  # lista 10 registrod=s na pagina


@ admin.register(Movimento)
class MovimentoAdmin(admin.ModelAdmin):
    list_display = ['get_formata_mesano_movimento', 'get_contasmovimento',
                    'get_tipo_calculomov', 'get_formatValorMov']
    list_per_page = 15  # lista 10 registrod=s na pagina
