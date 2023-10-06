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
        <p>Olá caro condômino {apto}. </p>
        <p>Segue anexo o demonstrativo do condominio do Mês Ano: {ma} </p>
        <p>Favor efetuar o pagamento até dia 10 do mes corrente. </p>
        <p></p>
        <p>Atenciosamente,</p>
        <p>Condominio das Palmeiras</p>
        '''
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


'''
def sendwhatsApp(request, ma, telefone, apto):
    CAMINHO_ARQUIVO = Path(__file__).parent
    caminho = CAMINHO_ARQUIVO / 'templates\emailer' / ma
    # caminho.touch #criar
    # caminho.unlink  # apagar
    caminho.mkdir(exist_ok=True)
    caminho = CAMINHO_ARQUIVO / 'templates\emailer' / \
        ma / f'{apto}.pdf'  # / arquivo
    # print(caminho)
    diretorio, nome_arquivo = os.path.split(caminho)
    print('ioioioioioioioioioioioi')
    print(caminho)
    print('fimfimfimfimfimfimfimfim')
    driver = webdriver.Chrome()
    driver.get('https://web.whatsapp.com/')

    telefone = ['4197034647']
    # Localize o campo de pesquisa do WhatsApp e pesquise o número de celular
    # search_xpath = '//*[@id="pane-side"]/button/div/div[2]/div/div'
    search_xpath = '//div[@contenteditable="true"][@data-tab="3"]'
    search_box = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, search_xpath)))
    search_box.clear()
    search_box.send_keys(telefone)
    search_box.send_keys(Keys.ENTER)

    # Aguarde até que o chat seja carregado
    chat_xpath = f'//div[@title="{telefone}"]'
    chat = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, chat_xpath)))
    chat.click()

    # Envie o arquivo PDF
    attachment_xpath = '//div[@title="Anexar"]'
    attachment_btn = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, attachment_xpath)))
    attachment_btn.click()

    file_xpath = '//input[@accept="image/*,video/mp4,video/3gpp,video/quicktime,application/pdf"]'
    file_input = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, file_xpath)))
    file_input.send_keys(caminho)

    time.sleep(2)  # Aguarde um pouco para o arquivo ser carregado

    send_btn_xpath = '//span[@data-icon="send"]'
    send_btn = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, send_btn_xpath)))
    send_btn.click()

    messages.success(request, ('WhatsApp sent successfully.'))

    return redirect('index')
'''
