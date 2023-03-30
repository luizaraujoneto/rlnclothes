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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["codnotafiscal"].widget.attrs["readonly"] = "readonly"
        self.fields["datanotafiscal"].widget = forms.DateInput(
            format="%Y-%m-%d", attrs={"type": "date"}
        )
        self.fields["observacao"].widget = forms.Textarea(attrs={"cols": 50, "rows": 4})
        self.fields["formapagamento"].widget.attrs = {"size": 48}


class ContasPagarForm(forms.ModelForm):
    class Meta:
        model = ContasPagar
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["codcontapagar"].widget.attrs["readonly"] = "readonly"
        self.fields["notafiscal"].widget = forms.HiddenInput()
        self.fields["observacao"].widget.attrs["width"] = "50"
        self.fields["formapagamento"].widget.attrs["width"] = "50"
        self.fields["datavencimento"].widget = forms.DateInput(
            format="%Y-%m-%d", attrs={"type": "date"}
        )
        self.fields["datapagamento"].widget = forms.DateInput(
            format="%Y-%m-%d", attrs={"type": "date"}
        )
