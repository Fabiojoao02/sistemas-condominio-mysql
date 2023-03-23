from django.contrib import admin
from . import models


class CalculosAdmin(admin.ModelAdmin):
    list_display = ['mesano',  'get_apto_salaCal', 'get_nome_moradorCal', 'get_contascalculo',
                    'get_formatvalorCal', 'publica', 'dt_lancamento']
    list_filter = ['mesano', 'id_morador', 'id_contas']
    list_per_page = 15  # lista 10 registrod=s na pagina
    search_fields = ['mesano', 'id_morador']


class LeiturasAdmin(admin.ModelAdmin):
    list_display = ['id_leituras', 'mesano', 'get_apto_salaLei', 'get_nome_moradorLei', 'get_contasleitura',
                    'get_formatvlgasm3', 'leitura_inicial', 'leitura_final', 'dt_leitura']
    list_per_page = 15  # lista 10 registrod=s na pagina


class MovimentoAdmin(admin.ModelAdmin):
    list_display = ['mesano', 'get_contasmovimento',
                    'get_tipo_calculomov', 'get_formatValorMov', 'dt_lancamento']
    list_per_page = 15  # lista 10 registrod=s na pagina


admin.site.register(models.Calculos, CalculosAdmin)
admin.site.register(models.Leituras, LeiturasAdmin)
admin.site.register(models.Movimento, MovimentoAdmin)
