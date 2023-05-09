# Enviando E-mails SMTP com Python
import os
import pathlib
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from string import Template
from django.shortcuts import redirect
from django.contrib import messages
from pathlib import Path
from email.mime.application import MIMEApplication


def sendemail(request, ma, email, apto):
    host = "smtp.gmail.com"
    port = 587
    login = 'condodaspalmeiras50@gmail.com'
    senha = 'zsgzaefsocmdtgrm'

    server = smtplib.SMTP(host, port)
    server.ehlo()
    server.starttls()
    server.login(login, senha)
    # class SendFormEmail(View):

    CAMINHO_ARQUIVO = Path(__file__).parent
    # print(CAMINHO_ARQUIVO)
    # mesano = ma
    # caminho = os.path.join(CAMINHO_ARQUIVO, 'templates\emailer', mesano)
    # arquivo = '301'+'.PDF'print()
    caminho = CAMINHO_ARQUIVO / 'templates\emailer' / ma
    # caminho.touch
    # caminho.unlink  # apagar
    caminho.mkdir(exist_ok=True)
    caminho = CAMINHO_ARQUIVO / 'templates\emailer' / \
        ma / f'{apto}.pdf'  # / arquivo
    # print(caminho)
    diretorio, nome_arquivo = os.path.split(caminho)
    # print(diretorio, nome_arquivo, email)

    corpo = f'Olá caro condômino {apto}. segue anexo o demonstrativo do condominio do Mês Ano: {ma}'
    email_msg = MIMEMultipart()
    email_msg['From'] = login
    email_msg['To'] = email
    email_msg['Subject'] = f'Demonstrativo condomínio Referente Mês Ano: {ma}'

    with open(caminho, 'rb') as f:
        attachment = MIMEApplication(f.read(), _subtype='pdf')
        attachment.add_header('Content-Disposition',
                              'attachment', filename=f'{apto}.pdf')

    email_msg.attach(attachment)

    email_msg.attach(MIMEText(corpo, 'plain'))
    server.sendmail(email_msg['From'], email_msg['To'], email_msg.as_string())

    server.quit()
    messages.success(request, ('Email sent successfully.'))

    return redirect('index')
