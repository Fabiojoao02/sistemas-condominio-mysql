from django.contrib import admin
from . import models


class BlocoInLine(admin.TabularInline):
    model = models.Bloco
    extra = 1


class CondominioAdmin(admin.ModelAdmin):
    list_display = ['nome', 'endereco', 'cidade',
                    'estado', 'bairro', 'cep', 'mostrar']
    # list_display_links = ['nome', 'Cidade', 'Estado']
    # list_filter = ['nome', 'Cidade', 'Estado']
    list_per_page = 10  # lista 10 registrod=s na pagina
    search_fields = ['nome', 'cidade', 'estado']
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

    def nome_morador(self, obj):
        return obj.cadastro.nome

    def cpf_cnpj_morador(self, obj):
        return obj.cadastro.cpf_cnpj

    def telefone_morador(self, obj):
        return obj.cadastro.telefone

    def email_morador(self, obj):
        return obj.cadastro.email

    list_display = ['nome_morador', 'apto_sala', 'cpf_cnpj_morador', 'telefone_morador',
                    'email_morador', 'nome_bloco', 'qt_moradores']


admin.site.register(models.Condominio, CondominioAdmin)
admin.site.register(models.Bloco, BlocoAdmin)
admin.site.register(models.Morador, MoradorAdmin)
