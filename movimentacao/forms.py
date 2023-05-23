from django import forms
from movimentacao.models import Leituras


class LeiturasForm(forms.ModelForm):
    class meta:
        model = Leituras
        fields = "__all__"
