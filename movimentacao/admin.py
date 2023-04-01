from django.contrib import admin
from . import models
from django.db.models import Sum
from .models import Leituras, Calculos, Movimento


@admin.register(Calculos)
class CalculosAdmin(admin.ModelAdmin):
    totalAlarmCount = Calculos.objects.filter(mesano='022023').values(
        'mesano', 'id_morador').annotate(total_valor=Sum('valor')).order_by('mesano', 'id_morador')

    list_display = ['get_formata_mesano_calculo',  'get_apto_salaCal', 'get_nome_moradorCal', 'get_contascalculo',
                    'get_formatvalorCal', 'publica']
    list_filter = ['mesano', 'id_morador', 'id_contas']
    list_per_page = 15  # lista 10 registrod=s na pagina
    search_fields = ['mesano', 'id_morador']


@admin.register(Leituras)
class LeiturasAdmin(admin.ModelAdmin):

    list_display = ['id_leituras', 'get_formata_mesano_leitura', 'get_apto_salaLei', 'get_nome_moradorLei', 'get_contasleitura',
                    'get_formatvlgasm3', 'leitura_inicial', 'leitura_final', 'dt_leitura']
    list_per_page = 15  # lista 10 registrod=s na pagina


@admin.register(Movimento)
class MovimentoAdmin(admin.ModelAdmin):
    list_display = ['get_formata_mesano_movimento', 'get_contasmovimento',
                    'get_tipo_calculomov', 'get_formatValorMov']
    list_per_page = 15  # lista 10 registrod=s na pagina
