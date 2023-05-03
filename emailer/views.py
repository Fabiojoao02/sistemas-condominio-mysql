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


def sendemail(request, ma, id_morador):
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
    mesano = ma
    # caminho = os.path.join(CAMINHO_ARQUIVO, 'templates\emailer', mesano)
    # arquivo = '301'+'.PDF'print()
    caminho = CAMINHO_ARQUIVO / 'templates\emailer' / ma
    # caminho.touch
    # caminho.unlink  # apagar
    caminho.mkdir(exist_ok=True)
    caminho = CAMINHO_ARQUIVO / 'templates\emailer' / ma / '301.pdf'  # / arquivo
    # print(caminho)
    diretorio, nome_arquivo = os.path.split(caminho)
    print(diretorio, nome_arquivo)

    corpo = 'Opa, Blz Garoto, estamos tendando anexar o email, nada não vai o anexo 2'
    email_msg = MIMEMultipart()
    email_msg['From'] = login
    email_msg['To'] = 'fabiojoaoanastacio@hotmail.com'
    email_msg['Subject'] = 'Meu Email enviado para teste com condominio'

    with open(caminho, 'rb') as f:
        attachment = MIMEApplication(f.read(), _subtype='pdf')
        attachment.add_header('Content-Disposition',
                              'attachment', filename="301.pdf")

    email_msg.attach(attachment)

    email_msg.attach(MIMEText(corpo, 'plain'))
    server.sendmail(email_msg['From'], email_msg['To'], email_msg.as_string())

    server.quit()
    messages.success(request, ('Email sent successfully.'))
    return redirect('index')


# email_msg.attach("301.pdf", attachment, "application/pdf")

'''
    # Mensagem de texto
    with open(caminho, 'r') as arquivo:
        texto_arquivo = arquivo.read()
        template = Template(texto_arquivo)
        texto_email = template.substitute(nome='Helena')

    # Transformar nossa mensagem em MIMEMultipart
    mime_multipart = MIMEMultipart()
    mime_multipart['from'] = settings.DEFAULT_FROM_EMAIL
    mime_multipart['to'] = 'fabiojoaoanastacio@hotmail.com'
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

    messages.success(request, ('Email sent successfully.'))
    return redirect('index')



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

#leitura documentos em anexo
for attachment in folder.iterdir():
    #envio de e-mail
    mail = outlook.CreateItem(0)
    mail.SentOnBehalfOfName = 'test@gmail.com.br'
    mail.HTMLBody = "<p>Olá,</p><p>Segue documentos em anexo.</p><p>Atenciosamente.</p>"
    mail.Attachments.Add(str(attachment))
    # coloca o nome do arquivo, sem a extnsão, como endereço do email antes do "@"
    mail.To = f'{attachment.stem}@gmail.com.br'
    mail.Subject = str(attachment)
    mail.display()
    time.sleep(5)
    mail.Send()    

'''
