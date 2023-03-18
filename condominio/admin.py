from django.contrib import admin
from . import models


class BlocoInLine(admin.TabularInline):
    model = models.Bloco
    extra = 1


class CondominioAdmin(admin.ModelAdmin):
    list_display = ['nome', 'Cidade', 'Estado',
                    'Bairro', 'Fracao_ideal_tem', 'get_Taxa_condominio', 'get_Fundo_reserva', 'mostrar']
    # list_display_links = ['nome', 'Cidade', 'Estado']
    # list_filter = ['nome', 'Cidade', 'Estado']
    list_per_page = 10  # lista 10 registrod=s na pagina
    search_fields = ['nome', 'Cidade', 'Estado']
    list_editable = ['mostrar']
    inlines = [
        BlocoInLine
    ]


class MoradorInLine(admin.TabularInline):
    model = models.Morador
    extra = 1


class BlocoAdmin(admin.ModelAdmin):
    list_display = ['nome']
    inlines = [
        MoradorInLine
    ]


class MoradorAdmin(admin.ModelAdmin):
    def nome_bloco(self, obj):
        return obj.bloco.nome

    list_display = ['nome', 'apto_sala', 'cpf', 'telefone',
                    'email', 'estado', 'nome_bloco']


admin.site.register(models.Condominio, CondominioAdmin)
admin.site.register(models.Bloco, BlocoAdmin)
admin.site.register(models.Morador, MoradorAdmin)
