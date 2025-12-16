from django import forms



from notasfiscais.models import NotasFiscais, ContasPagar
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit, Button, Div



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
        fields = [
            "codcontapagar",
            "notafiscal",
            "parcela",
            "datavencimento",
            "valorparcela",
            "datapagamento",
            "formapagamento",
            "observacao",
        ]
        labels = {
            "codcontapagar": "Cód. Conta Pagar",
            "notafiscal": "Nota Fiscal",
            "parcela": "Parcela",
            "datavencimento": "Data Vencimento",
            "valorparcela": "Valor Parcela",
            "datapagamento": "Data Pagamento",
            "formapagamento": "Forma Pagamento",
            "observacao": "Observação",
        }

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


class GerarParcelasContasPagarForm(forms.Form):
    """
    Formulário para geração automática de parcelas de Contas a Pagar.
    """
    descricao_parcela = forms.CharField(
        label='Descrição base para Parcela',
        max_length=255,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ex: Pagamento Fornecedor'
        }),
        help_text="Será concatenado com o número da parcela (ex: 'Pagamento Fornecedor - 1/5')"
    )

    formapagamento_input = forms.CharField(
        label='Forma de Pagamento',
        max_length=255,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ex: Boleto Bancário'
        })
    )
    
    data_primeira_parcela = forms.DateField(
        label='Data 1ª Parcela',
        required=True,
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control'
        })
    )
    
    num_parcelas = forms.IntegerField(
        label='Nº Parcelas',
        min_value=1,
        max_value=120,
        required=True,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ex: 12'
        })
    )
    
    observacao = forms.CharField(
        label='Observação',
        max_length=255,
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,
            'placeholder': 'Observações adicionais (opcional)'
        })
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            'descricao_parcela',
            'formapagamento_input',
            Row(
                Column('data_primeira_parcela', css_class='form-group col-md-6 mb-0'),
                Column('num_parcelas', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            'observacao',
            Div(
                Submit('submit', 'Gerar Parcelas', css_class='btn btn-success'),
                Button('cancel', 'Cancelar', css_class='btn btn-outline-danger', onclick="window.history.back()"),
                css_class='text-right mt-4'
            )
        )
