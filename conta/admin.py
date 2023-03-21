from django.contrib import admin
from . import models


class ContasAdmin(admin.ModelAdmin):
    list_display = ['id_conta', 'nome', 'situacao']
    list_per_page = 10  # lista 10 registrod=s na pagina


admin.site.register(models.Contas, ContasAdmin)
