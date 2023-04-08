from django import forms


from notasfiscais.models import NotasFiscais, ContasPagar


class NotasFiscaisForm(forms.ModelForm):
    class Meta:
        model = NotasFiscais
        fields = [
            "codnotafiscal",
            "numeronotafiscal",
            "fornecedor",
            "datanotafiscal",
            "valornotafiscal",
            "observacao",
            "formapagamento",
        ]

        labels = {
            "codnotafiscal": "Cód. Nota Fiscal",
            "numeronotafiscal": "Número Nota Fiscal",
            "fornecedor": "Fornecedor",
            "datanotafiscal": "Data Nota Fiscal",
            "valornotafiscal": "Valor Nota Fiscal",
            "observacao": "Observação",
            "formapagamento": "Forma de Pagamento",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        codnotafiscal = self.instance.codnotafiscal
        if codnotafiscal:
            self.fields["codnotafiscal"].widget.attrs = {
                "readonly": "readonly",
                "width": "50",
                "class": "form-control",
            }
        else:
            self.fields["codnotafiscal"].widget = forms.HiddenInput()

        self.fields["numeronotafiscal"].widget.attrs = {"class": "form-control"}
        self.fields["fornecedor"].widget.attrs = {"class": "form-control"}
        self.fields["datanotafiscal"].widget = forms.DateInput(
            format="%Y-%m-%d", attrs={"type": "date", "class": "form-control"}
        )
        self.fields["valornotafiscal"].widget.attrs = {
            "class": "form-control",
            "step": "0.01",
        }
        self.fields["observacao"].widget = forms.Textarea(
            attrs={"class": "form-control", "cols": 50, "rows": 4}
        )
        self.fields["formapagamento"].widget.attrs = {
            "class": "form-control",
            "size": 48,
        }


class ContasPagarForm(forms.ModelForm):
    class Meta:
        model = ContasPagar
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        codcontapagar = self.instance.codcontapagar
        if codcontapagar:
            self.fields["codcontapagar"].widget.attrs = {
                "readonly": "readonly",
                "width": "50",
                "class": "form-control",
            }
        else:
            self.fields["codcontapagar"].widget = forms.HiddenInput()

        self.fields["notafiscal"].widget = forms.HiddenInput()
        self.fields["parcela"].widget.attrs = {"class": "form-control", "width": 150}
        self.fields["formapagamento"].widget.attrs = {
            "class": "form-control",
            "width": 50,
        }
        self.fields["datavencimento"].widget = forms.DateInput(
            format="%Y-%m-%d", attrs={"type": "date", "class": "form-control"}
        )
        self.fields["datapagamento"].widget = forms.DateInput(
            format="%Y-%m-%d", attrs={"type": "date", "class": "form-control"}
        )
        self.fields["observacao"].widget = forms.Textarea(
            attrs={"class": "form-control", "cols": 50, "rows": 4}
        )
        self.fields["valorparcela"].widget.attrs = {
            "class": "form-control",
            "step": "0.01",
        }
