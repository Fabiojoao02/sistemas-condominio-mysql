from django.contrib import admin
from . import models


class CalculosAdmin(admin.ModelAdmin):
    list_display = ['get_formata_mesano_calculo',  'get_apto_salaCal', 'get_nome_moradorCal', 'get_contascalculo',
                    'get_formatvalorCal', 'publica', 'dt_lancamento']
    list_filter = ['mesano', 'id_morador', 'id_contas']
    list_per_page = 15  # lista 10 registrod=s na pagina
    search_fields = ['mesano', 'id_morador']


class LeiturasAdmin(admin.ModelAdmin):
    # for leitura in list(['get_count']):
    #     print(leitura.split(list(['get_count'])))

    #     print('fffffffffffffffffffffffffffffffffffffffffffffiioioioioioioi')
    #     print(leitura)

    #     print(i)

    # get_count()

    # list_display = ['get_count']

    list_display = ['id_leituras', 'get_formata_mesano_leitura', 'get_apto_salaLei', 'get_nome_moradorLei', 'get_contasleitura',
                    'get_formatvlgasm3', 'leitura_inicial', 'leitura_final', 'dt_leitura']
    list_per_page = 15  # lista 10 registrod=s na pagina
    list_filter = ['mesano', 'id_leituras']


class MovimentoAdmin(admin.ModelAdmin):
    list_display = ['get_formata_mesano_movimento', 'get_contasmovimento',
                    'get_tipo_calculomov', 'get_formatValorMov', 'dt_lancamento']
    list_per_page = 15  # lista 10 registrod=s na pagina


admin.site.register(models.Calculos, CalculosAdmin)
admin.site.register(models.Leituras, LeiturasAdmin)
admin.site.register(models.Movimento, MovimentoAdmin)
