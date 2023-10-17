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

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.common.keys import Keys
import pyautogui
from utils import utils


def sendemail(request, ma, email, apto):

    try:
        host = "smtp.gmail.com"
        port = 587  # 465  # 587
        login = 'condodaspalmeiras50@gmail.com'
        senha = 'ikywlvlglvccymuo'
        server = smtplib.SMTP(host, port)
        server.ehlo()
        server.starttls()
        server.login(login, senha)
        CAMINHO_ARQUIVO = Path(__file__).parent
        caminho = CAMINHO_ARQUIVO / 'templates\emailer' / ma
        # caminho.touch #criar
        # caminho.unlink  # apagar
        caminho.mkdir(exist_ok=True)
        caminho = CAMINHO_ARQUIVO / 'templates\emailer' / \
            ma / f'{apto}.pdf'  # / arquivo
        # print(caminho)
        diretorio, nome_arquivo = os.path.split(caminho)

        corpo = f'''
        <h3>Demonstrativo</h3>
        <p></p>
        <p>Olá caro condômino {apto}. </p>
        <p>Segue anexo o demonstrativo do condominio do Mês Ano: {utils.formata_mesano(ma)} </p>
        <p><h3>Atenção: Favor efetuar o pagamento até dia 10 do mes corrente. </h3></p>
        <p></p>
        <p></p>
        <p>Atenciosamente,</p>
        <p>Condominio das Palmeiras</p>
        '''
        email_msg = MIMEMultipart()
        email_msg['From'] = login
        email_msg['To'] = email
        email_msg[
            'Subject'] = f'Demonstrativo condomínio Referente Mês Ano: {utils.formata_mesano(ma)} '

        with open(caminho, 'rb') as f:
            attachment = MIMEApplication(f.read(), _subtype='pdf')
            attachment.add_header('Content-Disposition',
                                  'attachment', filename=f'{apto}.pdf')

        email_msg.attach(attachment)

        email_msg.attach(MIMEText(corpo, 'html'))
        server.sendmail(email_msg['From'],
                        email_msg['To'], email_msg.as_string())

        server.quit()
        messages.success(request, ('Email sent successfully.'))

    except smtplib.SMTPException as e:
        # Exceção genérica do SMTP
        messages.error(
            request, ('Ocorreu um erro ao enviar o email: 'f'{e}'))

    except smtplib.SMTPServerDisconnected as e:
        # Servidor SMTP desconectado inesperadamente
        messages.error(
            request, ('O servidor SMTP foi desconectado inesperadamente:: 'f'{e}'))

    except smtplib.SMTPResponseException as e:
        # Exceção de resposta do servidor SMTP
        messages.error(
            request, ('O servidor SMTP retornou um erro: 'f'{e.smtp_code},{e.smtp_error}'))

    except Exception as e:
        # Outras exceções
        messages.error(
            request, ('Ocorreu um erro inesperado: 'f'{e}'))
        print('Ocorreu um erro inesperado: ', e)

    # finally:

    return redirect('index')


def sendemailgerencial(request, ma, email, idb, apto):

    try:
        host = "smtp.gmail.com"
        port = 587  # 465  # 587
        login = 'condodaspalmeiras50@gmail.com'
        senha = 'ikywlvlglvccymuo'
        server = smtplib.SMTP(host, port)
        server.ehlo()
        server.starttls()
        server.login(login, senha)
        CAMINHO_ARQUIVO = Path(__file__).parent
        caminho = CAMINHO_ARQUIVO / 'templates\emailer' / ma
        # caminho.touch #criar
        # caminho.unlink  # apagar
        caminho.mkdir(exist_ok=True)
        caminho = CAMINHO_ARQUIVO / 'templates\emailer' / \
            ma / f'{ma}_{idb}.pdf'  # / arquivo
        # print(caminho)
        diretorio, nome_arquivo = os.path.split(caminho)

        corpo = f'''
        <h3>Relatório gerencial</h3>
        <p>Olá caro proprietário Sr(a). {apto}. </p>
        <p>Segue anexo o relatório gerencial do condominio do Mês Ano: {utils.formata_mesano(ma)} </p>
        <p></p>
        <p></p>
        <p>Atenciosamente,</p>
        <p>Condominio das Palmeiras</p>
        '''
        email_msg = MIMEMultipart()
        email_msg['From'] = login
        email_msg['To'] = email
        email_msg[
            'Subject'] = f'Relatório gerencial  Referente Mês Ano: {utils.formata_mesano(ma)}'

        with open(caminho, 'rb') as f:
            attachment = MIMEApplication(f.read(), _subtype='pdf')
            attachment.add_header('Content-Disposition',
                                  'attachment', filename=f'{apto}.pdf')

        email_msg.attach(attachment)

        email_msg.attach(MIMEText(corpo, 'html'))
        server.sendmail(email_msg['From'],
                        email_msg['To'], email_msg.as_string())

        server.quit()
        messages.success(request, ('Email sent successfully.'))

    except smtplib.SMTPException as e:
        # Exceção genérica do SMTP
        messages.error(
            request, ('Ocorreu um erro ao enviar o email: 'f'{e}'))

    except smtplib.SMTPServerDisconnected as e:
        # Servidor SMTP desconectado inesperadamente
        messages.error(
            request, ('O servidor SMTP foi desconectado inesperadamente:: 'f'{e}'))

    except smtplib.SMTPResponseException as e:
        # Exceção de resposta do servidor SMTP
        messages.error(
            request, ('O servidor SMTP retornou um erro: 'f'{e.smtp_code},{e.smtp_error}'))

    except Exception as e:
        # Outras exceções
        messages.error(
            request, ('Ocorreu um erro inesperado: 'f'{e}'))
        print('Ocorreu um erro inesperado: ', e)

    # finally:
       # Construa a nova URL com o novo parâmetro
    nova_url = f'/listaconblomov/{idb}/'

    # messages.success(request, ('Email sent successfully.'))
    return redirect(nova_url)
