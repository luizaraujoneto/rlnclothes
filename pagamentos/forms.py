from django import forms

from pagamentos.models import Pagamentos

from datetime import datetime

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

    NUM_PARCELAS_CHOICES = [(i, str(i)) for i in range(1, 6)]
    
    numparcelas = forms.ChoiceField(
        choices=NUM_PARCELAS_CHOICES,
        label="Número de Parcelas",
        required=False
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["codpagamento"].widget = forms.HiddenInput()
        self.fields["cliente"].widget = forms.HiddenInput()
        self.fields["tipopagamento"].widget = forms.RadioSelect(
            choices=Pagamentos.TIPOS_PAGAMENTO,
            attrs={"class": "form-check-inline"},
        )
        self.fields["datapagamento"].widget = forms.DateInput(
            format="%Y-%m-%d", attrs={"type": "date", "class": "form-control"}
        )
        self.fields["observacao"].widget = forms.Textarea(
            attrs={"cols": 50, "rows": 4, "class": "form-control"}
        )
        self.fields["valorpagamento"].widget.attrs = {
            "class": "form-control",
            "step": "0.01",
        }
        self.fields["formapagamento"].widget.attrs = {
            "size": "45",
            "class": "form-control",
        }

        codpagamento = self.initial.get("codpagamento")

        if codpagamento:
            self.fields["numparcelas"].widget = forms.HiddenInput()
        else:
            self.fields["numparcelas"].widget.attrs = {
                "class": "form-control",
        }



