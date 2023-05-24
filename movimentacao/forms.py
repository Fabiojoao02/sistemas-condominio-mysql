from django import forms
from movimentacao.models import Leituras


class LeiturasForm(forms.ModelForm):
    leitura_final = forms.CharField(required=False)

    class Meta:
        model = Leituras
        fields = [
            'mesano',
            'id_morador',
            'id_contas',
            'leitura_final',
        ]
