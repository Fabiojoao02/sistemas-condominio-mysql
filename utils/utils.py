def formata_valor(val):
    return f'{val:.2f}'.replace('.', ',')


def formata_mesano(texto):
    return texto[0:2] + '/' + texto[2:6]
