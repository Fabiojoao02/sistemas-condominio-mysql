from django import forms
from django.forms import ModelForm
from movimentacao.models import Leituras, Movimento, Calculos
from conta.models import Contas
from condominio.models import Morador, Bloco, Cadastro
# from tempus_dominus.widgets import DatePicker
from datetime import datetime
from django.db.models import QuerySet
from django.db import connection


class LeiturasForm(ModelForm):

    leitura_final = forms.CharField(required=False)
    dt_leitura = forms.CharField(required=False)
    id_contas = forms.ModelChoiceField(
        queryset=Contas.objects.filter(leituras=1),
        empty_label=None,
        # required=False,
        widget=forms.Select(
            attrs={'class': 'form-control', 'placeholder': 'Codigo Conta'})
    )

    data_leitura = Leituras.objects.first()
    dt_leitura = forms.DateField(widget=forms.DateInput(
        attrs={'type': 'date', 'max': datetime.now(), 'value': data_leitura}), initial=data_leitura)

    id_morador = forms.ModelChoiceField(
        queryset=Morador.objects.filter(id_inquilino__isnull=False).order_by(
            'apto_sala', 'id_inquilino__nome'),
        empty_label=None,
        # required=False,
        widget=forms.Select(
            attrs={'class': 'form-control', 'placeholder': 'Morador'})
    )

    class Meta:
        model = Leituras
        fields = (
            # 'id_bloco',
            'id_morador',
            'id_contas',
            'dt_leitura',
            'valor_m3',
            'leitura_final',
        )
        labels = {
            # 'id_bloco': '',
            'id_morador': '',
            'id_contas': '',
            'dt_leitura': '',
            'valor_m3': '',
            'leitura_final': '',
        }

        widgets = {
            'id_morador': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Codigo Morador'}),
            'valor_m3': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Valor M3'}),
            'leitura_final': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Leituras'}),
        }


class CalculosForm(ModelForm):

    class Meta:
        model = Calculos
        fields = (
            # 'id_morador',
            'pago',

        )


class AutorizaCalculoForm(ModelForm):
    responsavel = forms.CharField(required=True)

    class Meta:
        model = Movimento
        fields = [
            'responsavel',
        ]

        error_messages = {
            "responsavel": {
                "required": "Por favor, informe o nome do responsável pelo calculo referênte"
            }

        }
