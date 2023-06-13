from django import forms
from django.forms import ModelForm
from movimentacao.models import Leituras, Movimento
from conta.models import Contas
from condominio.models import Morador,Bloco, Cadastro
#from tempus_dominus.widgets import DatePicker
from datetime import datetime
from django.db.models import QuerySet
from django.db import connection


class LeiturasForm(ModelForm):

    # moradores = Morador.objects.raw('''
    #       select  m.id_morador,  concat(m.apto_sala,'-', cad.nome) morador
    #       from morador m
    #       join cadastro cad on
    #        cad.id_cadastro = case when responsavel='I' then id_inquilino else id_proprietario end
    #       where m.id_bloco =   2
    #           group by  m.apto_sala, cad.nome
    #           order by apto_sala
    #       ''')

   # queryset = QuerySet(model=Morador)
    # Carregar a lista de moradores no cache interno
    # queryset._result_cache = list(moradores)

    # print(queryset)

    # print(registros_origem)
   #id_bloco = forms.ModelChoiceField(
   #    queryset=Bloco.objects.all().order_by('id_bloco'),
   #    empty_label=None,
   #    widget=forms.Select(
   #        attrs={'class': 'form-control', 'placeholder': 'Bloco'})
   #)   
    leitura_final = forms.CharField(required=False)
    #leitura_inicial = forms.CharField(required=Leituras.leitura_inicial)
    id_contas = forms.ModelChoiceField(
        queryset=Contas.objects.filter(leituras=1),
        empty_label=None,
        widget=forms.Select(
            attrs={'class': 'form-control', 'placeholder': 'Codigo Conta'})
    )

    dt_leitura = forms.DateField(widget=forms.DateInput(
        attrs={'type': 'date', 'max': datetime.now()}))

   # id_morador = forms.ModelChoiceField(
   #     queryset=Morador.objects.all().order_by('apto_sala'),
   #     empty_label=None,
   #     widget=forms.Select(
   #         attrs={'class': 'form-control', 'placeholder': 'Morador'})
   # )

    id_morador = forms.ModelChoiceField(
        #queryset=Morador.objects.filter(id_inquilino__isnull=False).order_by('apto_sala', 'id_inquilino__nome'),
        queryset=Morador.objects.filter(id_inquilino__isnull=False).order_by('id_inquilino__apto_sala', 'id_inquilino__id_inquilino__nome'),
        empty_label=None,
        widget=forms.Select(
            attrs={'class': 'form-control', 'placeholder': 'Morador'})
    )

    def label_from_instance(self, obj):
        return f'{obj.id_inquilino.apto_sala}-{obj.id_inquilino.id_inquilino.nome}'


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
           # 'id_bloco': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Bloco'}),
            'id_morador': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Codigo Morador'}),
            # 'id_contas': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Codigo Conta'}),
            # 'dt_leitura': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Data Leitura'}),
            # 'valor_m3': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Valor M3'}),
            # 'leitura_inicial': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Leitura Inicial'}),
            'leitura_final': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Leituras'}),
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
