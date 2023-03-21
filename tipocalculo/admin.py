from django.contrib import admin
from . import models


class TipoCalculoAdmin(admin.ModelAdmin):
    list_display = ['id_tipo_calculo', 'nome', 'descricao', 'situacao']
    list_per_page = 10  # lista 10 registrod=s na pagina


admin.site.register(models.TipoCalculo, TipoCalculoAdmin)
