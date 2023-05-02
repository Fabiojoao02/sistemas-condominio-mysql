# from django.shortcuts import render
import os
from django.views.generic import View
from django.shortcuts import redirect
from django.contrib import messages
from django.core.mail import send_mail, send_mass_mail, EmailMessage
from django.conf import settings
from pathlib import Path
import shutil

from condominio.views import listaconblomorador
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# from django.template.loader import get_template, render_to_string


class SendFormEmail(View):

    def get(self, request):

        # print(Path.home())

        CAMINHO_ARQUIVO = Path(__file__).parent
        mesano = '022023'
        # caminho = os.path.join(CAMINHO_ARQUIVO, 'templates\emailer', mesano)
        # arquivo = '301'+'.PDF'
        caminho = CAMINHO_ARQUIVO / 'templates\emailer' / mesano
        # caminho.touch
        # caminho.unlink  # apagar
        caminho.mkdir(exist_ok=True)
        caminho = CAMINHO_ARQUIVO / 'templates\emailer' / mesano  # / arquivo
        # print(caminho)
       #
       # listaconblomorador(request, idb, ma)
       # for i in range(10):
       #     arquivo = caminho / f'file_{i}.pdf'
       #     if arquivo.exists():
       #         arquivo.unlink()  # deleta
       #     else:
       #         arquivo.touch()  # cria

      #  print(CAMINHO_ARQUIVO)

        # Get the form data
        name = request.GET.get('name', None)
        email = request.GET.get('email', None)
        message = request.GET.get('message', None)

        send_mail(
            'subject',
            'body of the message',
            'fbianastacio@gmail.com',
            [
                'fabiojoaoanastacio@hotmail.com',
                'fabio.joao@fbin.com.br'
            ],
            fail_silently=False,
            # html_message=msg,
        )

        messages.success(request, ('Email sent successfully.'))
        return redirect('index')
