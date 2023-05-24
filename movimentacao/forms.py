from django import forms
from movimentacao.models import Leituras


class LeiturasForm(forms.ModelForm):
    class Meta:
        model = Leituras
        fields = '__all__'
