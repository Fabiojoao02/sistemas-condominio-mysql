from django import forms
from django.forms import ModelForm
from movimentacao.models import Leituras


class LeiturasForm(ModelForm):
    leitura_final = forms.CharField(required=False)

    class Meta:
        model = Leituras
        # mesano,id_bloco,id_morador,id_contas,dt_leitura,valor_m3,leitura_inicial,leitura_final
        fields = [
            'mesano',
            'id_bloco',
            'id_morador',
            'id_contas',
            'dt_leitura',
            'valor_m3',
            'leitura_inicial',
            'leitura_final',
        ]
