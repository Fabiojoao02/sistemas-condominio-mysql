from django import forms
from django.forms import ModelForm
from movimentacao.models import Leituras, Movimento
from conta.models import Contas
from tempus_dominus.widgets import DatePicker
from datetime import datetime


class LeiturasForm(ModelForm):

    # registros_origem = Contas.objects.filter(Leituras__valor=1)

    # print(registros_origem)
    leitura_final = forms.CharField(required=False)
    leitura_inicial = forms.CharField(required=Leituras.leitura_inicial)
    id_contas = forms.ModelChoiceField(
        queryset=Contas.objects.filter(leituras=1),
        empty_label=None,
        widget=forms.Select(
            attrs={'class': 'form-control', 'placeholder': 'Codigo Conta'})
    )

    dt_leitura = forms.DateField(widget=forms.DateInput(
        attrs={'type': 'date', 'max': datetime.now()}))

    class Meta:
        model = Leituras
        fields = (
            'id_morador',
            'id_contas',
            'dt_leitura',
            'valor_m3',
            'leitura_inicial',
            'leitura_final',
        )
        labels = {
            'id_morador': '',
            'id_contas': '',
            'dt_leitura': '',
            'valor_m3': '',
            'leitura_inicial': '',
            'leitura_final': '',
        }

        widgets = {
            'id_morador': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Codigo Morador'}),
            # 'id_contas': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Codigo Conta'}),
            # 'dt_leitura': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Data Leitura'}),
            'valor_m3': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Valor M3'}),
            'leitura_inicial': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Leitura Inicial'}),
            'leitura_final': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Leitura Final'}),
        }


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
