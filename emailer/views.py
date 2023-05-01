# from django.shortcuts import render
# import os
from django.views.generic import View
from django.shortcuts import redirect
from django.contrib import messages
from django.core.mail import send_mail, send_mass_mail, EmailMessage
from django.conf import settings
# from django.template.loader import get_template, render_to_string


class SendFormEmail(View):

    def get(self, request):

        # Get the form data
        name = request.GET.get('name', None)
        email = request.GET.get('email', None)
        message = request.GET.get('message', None)

        send_mail(
            'subject',
            'body of the message',
            settings.DEFAULT_FROM_EMAIL,
            [
                'fabiojoaoanastacio@hotmail.com',
                'fabio.joao@fbin.com.br'
            ],
            fail_silently=False,
            # html_message=msg,
        )

        messages.success(request, ('Email sent successfully.'))
        return redirect('index')
