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
            "datavenda",
            "produto",
            "valorvenda",
            "observacao",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["codvenda"].widget.attrs["readonly"] = "readonly"
        self.fields["datavenda"].widget = forms.DateInput(attrs={"type": "date"})
        self.fields["observacao"].widget = forms.Textarea(attrs={"cols": 50, "rows": 4})


"""

class ItemVendaForm(forms.ModelForm):
    class Meta:
        model = ItemVenda
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["coditemvenda"].widget.attrs["readonly"] = "readonly"
        self.fields["venda"].widget = forms.HiddenInput()
        # self.fields["descricao"].widget.attrs["width"] = "50"

"""
