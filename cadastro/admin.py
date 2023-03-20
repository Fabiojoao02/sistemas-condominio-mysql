from django.contrib import admin
from . import models


class CadastroAdmin(admin.ModelAdmin):
    list_display = ['nome', 'endereco', 'cidade', 'estado',
                    'bairro', 'telefone', 'email']
    list_per_page = 10  # lista 10 registrod=s na pagina


admin.site.register(models.Cadastro, CadastroAdmin)
