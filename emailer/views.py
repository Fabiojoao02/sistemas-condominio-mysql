# Enviando E-mails SMTP com Python
# import os
import pathlib
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from string import Template
from django.shortcuts import redirect
from django.contrib import messages
from django.conf import settings
from pathlib import Path

# from dotenv import load_dotenv  # type: ignore

# load_dotenv()


# class SendFormEmail(View):

def sendemail(request, ):

    CAMINHO_ARQUIVO = Path(__file__).parent
    mesano = '022023'
    # caminho = os.path.join(CAMINHO_ARQUIVO, 'templates\emailer', mesano)
    # arquivo = '301'+'.PDF'
    caminho = CAMINHO_ARQUIVO / 'templates\emailer' / mesano
    # caminho.touch
    # caminho.unlink  # apagar
    caminho.mkdir(exist_ok=True)
    caminho = CAMINHO_ARQUIVO / 'templates\emailer' / mesano / '301.pdf'  # / arquivo
    print(caminho)

    messages.success(request, ('Email sent successfully.'))
    return redirect('index')


"""
    # Dados do remetente e destinatário
    remetente = settings.DEFAULT_FROM_EMAIL
    destinatario = remetente

    # Configurações SMTP
    smtp_server = settings.EMAIL_HOST
    smtp_port = 587
    smtp_username = settings.EMAIL_HOST_USER
    smtp_password = settings.EMAIL_HOST_PASSWORD

    # Mensagem de texto
    with open(CAMINHO_HTML, 'r') as arquivo:
        texto_arquivo = arquivo.read()
        template = Template(texto_arquivo)
        texto_email = template.substitute(nome='Helena')

    # Transformar nossa mensagem em MIMEMultipart
    mime_multipart = MIMEMultipart()
    mime_multipart['from'] = remetente
    mime_multipart['to'] = destinatario
    mime_multipart['subject'] = 'Este é o assunto do e-mail'

    corpo_email = MIMEText(texto_email, 'html', 'utf-8')
    mime_multipart.attach(corpo_email)

    # Envia o e-mail
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.ehlo()
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.send_message(mime_multipart)
        print('E-mail enviado com  sucesso!')
"""
# messages.success(request, ('Email sent successfully.'))
# return redirect('index')
