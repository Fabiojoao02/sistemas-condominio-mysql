from django.template import Library
from utils import utils
from movimentacao.models import Leituras
from django.db.models import Sum

register = Library()


@register.filter
def formata_valor(val):
    return utils.formata_valor(val)


@register.filter
def formata_mesano(texto):
    return utils.formata_mesano(texto)


@register.filter
def consumo_leitura(val):
    leitura = Leituras.objects.get(id_leituras=val)
    consumo = leitura.leitura_final - leitura.leitura_inicial
    return f'{consumo:.3f}'.replace('.', ',')


@register.filter
def valor_consumo_leitura(val):
    leitura = Leituras.objects.get(id_leituras=val)
    consumo = leitura.leitura_final - leitura.leitura_inicial
    valor = consumo * leitura.vl_gas_m3
    return f'{valor:.2f}'.replace('.', ',')
