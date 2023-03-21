from django.contrib import admin
from . import models
from django.utils.html import format_html


class BlocoInLine(admin.TabularInline):
    model = models.Bloco
    extra = 1


class CondominioAdmin(admin.ModelAdmin):
    list_display = ['nome', 'cidade', 'estado',
                    'bairro', 'mostrar',  'foto_preview']
    # list_display_links = ['nome', 'Cidade', 'Estado']
    # list_filter = ['nome', 'Cidade', 'Estado']
    list_per_page = 10  # lista 10 registrod=s na pagina
    search_fields = ['nome', 'cidade', 'estado']
    list_editable = ['mostrar']
    inlines = [
        BlocoInLine
    ]

    def foto_preview(self, obj):
        return format_html(
            f"<img src='{obj.foto.url}' width='{obj.foto.width}' height='{obj.foto.height}' style='border-radius: 5% 5%;'/>")

    readonly_fields = ['foto_preview']


class MoradorInLine(admin.TabularInline):
    model = models.Morador
    extra = 1


class BlocoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'get_Taxa_condominio',
                    'get_Fundo_reserva', 'get_Fracao_ideal']
    inlines = [
        MoradorInLine
    ]


class MoradorAdmin(admin.ModelAdmin):
    list_display = ['apto_sala',  'get_nome_inquilino', 'get_cpf_cnpj_morador', 'get_telefone_morador',
                    'get_email_morador', 'get_nome_proprietario', 'get_nome_bloco', 'foto']


admin.site.register(models.Condominio, CondominioAdmin)
admin.site.register(models.Bloco, BlocoAdmin)
admin.site.register(models.Morador, MoradorAdmin)
# admin.site.register(models.Cadastro, CadastroAdmin)
