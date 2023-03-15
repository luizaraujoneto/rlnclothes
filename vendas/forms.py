from django import forms

from fornecedores.models import Fornecedores
from notasfiscais.models import NotasFiscais
from vendas.models import Vendas  # , ItemVenda


class VendasForm(forms.ModelForm):
    class Meta:
        model = Vendas
        fields = [
            "codvenda",
            "cliente",
            "produto",
            "datavenda",
            "valorvenda",
            "observacao",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["codvenda"].widget = forms.HiddenInput()
        self.fields["cliente"].widget = forms.HiddenInput()
        self.fields["datavenda"].widget = forms.DateInput(attrs={"type": "date"})
        self.fields["observacao"].widget = forms.Textarea(attrs={"cols": 50, "rows": 4})
