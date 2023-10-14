def formata_valor(val):
    texto_valor = f'{val:_.2f}'
    texto_valor = texto_valor.replace('.', ',').replace('_', '.')
    return texto_valor


def formata_valorm3(val):
    texto_valor = f'{val:_.3f}'
    texto_valor = texto_valor.replace('.', ',').replace('_', '.')
    return texto_valor


def formata_data(val):
    return f' {val.strftime("%d/%m/%Y")}'


def formata_mesano(texto):
    return texto[0:2] + '/' + texto[2:6]


def draw_gauge(c, percent):
    # Define as coordenadas e dimensões do medidor
    x, y = 150, 600
    width, height = 300, 30

    # Define as cores
    fill_color = (1, 1, 1)  # Branco
    border_color = (0, 0, 1)  # Azul

    # Desenha o medidor
    c.setFillColorRGB(*fill_color)
    c.setStrokeColorRGB(*border_color)
    c.rect(x, y, width, height, fill=1)

    # Calcula a largura da barra com base no percentual
    bar_width = percent * width / 100

    # Desenha a barra de progresso
    c.setFillColorRGB(*border_color)
    c.rect(x, y, bar_width, height, fill=1)

    # Define a fonte e o tamanho do texto
    c.setFont("Helvetica", 12)

    # Calcula a posição para o texto (centro do medidor)
    text_x = x + (width - c.stringWidth(f"{percent}%", "Helvetica", 12)) / 2
    text_y = y + (height - 12) / 2

    # Define as cores
    green_color = (0, 1, 0)  # Verde
    yellow_color = (1, 1, 0)  # Amarelo
    red_color = (1, 0, 0)  # Vermelho

    if percent > 75:
        # Define a cor do texto para vermelho
        c.setFillColorRGB(1, 0, 0)
    elif percent in (50, 75):
        # Define a cor do texto para amarelo
        c.setFillColorRGB(1, 1, 0)
    else:
        # Define a cor do texto para verde
        c.setFillColorRGB(0, 1, 0)

    # Desenha o texto no centro
    c.drawString(text_x, text_y, f"{percent}%")
