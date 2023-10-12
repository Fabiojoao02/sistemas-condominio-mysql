def formata_valor(val):
    texto_valor = f'{val:_.2f}'
    texto_valor = texto_valor.replace('.', ',').replace('_', '.')
    return texto_valor


def formata_valorm3(val):
    texto_valor = f'{val:_.3f}'
    texto_valor = texto_valor.replace('.', ',').replace('_', '.')
    return texto_valor


def formata_mesano(texto):
    return texto[0:2] + '/' + texto[2:6]
