from django import forms

from pagamentos.models import Pagamentos


class PagamentosForm(forms.ModelForm):
    class Meta:
        model = Pagamentos
        fields = [
            "codpagamento",
            "cliente",
            "tipopagamento",
            "formapagamento",
            "datapagamento",
            "valorpagamento",
            "observacao",
        ]
        labels = {
            "codpagamento": "Cód. Pgto.",
            "cliente": "Cliente",
            "tipopagamento": "Tipo Pgto.",
            "formapagamento": "Descrição",
            "datapagamento": "Data Pgto.",
            "valorpagamento": "Valor Pgto.",
            "observacao": "Observação",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["codpagamento"].widget = forms.HiddenInput()
        self.fields["cliente"].widget = forms.HiddenInput()
        self.fields["tipopagamento"].widget = forms.RadioSelect(
            choices=Pagamentos.TIPOS_PAGAMENTO
        )
        self.fields["datapagamento"].widget = forms.DateInput(
            attrs={"type": "date"}, format="%d/%m/%Y"
        )
        self.fields["observacao"].widget = forms.Textarea(attrs={"cols": 50, "rows": 4})
        self.fields["formapagamento"].widget.attrs["size"] = "45"
