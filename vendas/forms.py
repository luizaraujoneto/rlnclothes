from django import forms

from vendas.models import Vendas


class VendasForm(forms.ModelForm):
    info = forms.CharField()

    class Meta:
        model = Vendas
        fields = [
            "codvenda",
            "cliente",
            "produto",
            "info",
            "datavenda",
            "valorvenda",
            "observacao",
        ]

        labels = {
            "codvenda": "Cód. Venda",
            "cliente": "Cliente",
            "produto": "Produto",
            "datavenda": "Data Venda",
            "valorvenda": "Valor Venda",
            "observacao": "Observação",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["codvenda"].widget = forms.HiddenInput()
        self.fields["cliente"].widget = forms.HiddenInput()
        self.fields["produto"].widget.attrs = {"class": "form-control"}
        self.fields["info"].widget = forms.TextInput(
            attrs={"readonly": True, "class": "form-control", "disabled": True}
        )

        self.fields["datavenda"].widget = forms.DateInput(
            format="%Y-%m-%d", attrs={"type": "date", "class": "form-control"}
        )
        self.fields["valorvenda"].widget.attrs = {
            "class": "form-control",
            "step": "0.01",
        }
        self.fields["observacao"].widget = forms.Textarea(
            attrs={"cols": 50, "rows": 4, "class": "form-control"}
        )
