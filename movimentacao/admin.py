from django.contrib import admin
# from . import models
from django.db.models import Sum
from .models import Leituras, Calculos, Movimento, Cadastro, MovimentoMSG, MovimentoAnexos
from django.db import connection


@admin.register(Calculos)
class CalculosAdmin(admin.ModelAdmin):
    list_display = ('get_formata_mesano_calculo', 'get_apto_salaCal',
                    'get_nome_moradorCal', 'get_contascalculo', 'get_formatvalorCal')
    list_per_page = 15  # lista 10 registrod=s na pagina
    list_filter = [
        'mesano',
        'id_morador',
        'id_contas',
    ]


@ admin.register(Leituras)
class LeiturasAdmin(admin.ModelAdmin):

    list_display = ['id_leituras', 'get_formata_mesano_leitura', 'get_apto_salaLei', 'get_nome_moradorLei', 'get_contasleitura',
                    'get_formatvalorm3', 'leitura_inicial', 'leitura_final', 'get_dt_leitura_formatada']
    list_per_page = 15  # lista 10 registrod=s na pagina
    list_filter = [
        'mesano',
        'id_morador',
    ]


@ admin.register(Movimento)
class MovimentoAdmin(admin.ModelAdmin):
    list_display = ['get_formata_mesano_movimento', 'get_contasmovimento',
                    'get_tipo_calculomov', 'get_formatValorMov']
    list_per_page = 15  # lista 10 registrod=s na pagina
    list_filter = [
        'mesano',
        'id_bloco',
    ]


@ admin.register(MovimentoMSG)
class MovimentoAdminMSG(admin.ModelAdmin):
    list_display = ['mesano', 'mensagem']
    list_per_page = 15  # lista 10 registrod=s na pagina


@ admin.register(MovimentoAnexos)
class MovimentoAdminAnexos(admin.ModelAdmin):
    list_display = ['id_bloco',
                    'get_formata_mesano_movimento_anexo', 'descricao', 'situacao', 'anexo']
    list_per_page = 15  # lista 10 registrod=s na pagina
