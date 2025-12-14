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


from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit, Button, Div

class GerarParcelasForm(forms.Form):
    """
    Formulário para geração automática de parcelas de pagamento.
    """
    TIPO_CHOICES = [
        ('completo', 'Saldo Completo'),
        ('saldo_nao_previsto', 'Saldo ainda não parcelado'),
    ]
    
    tipopgto = forms.ChoiceField(
        label='Tipo Pgto.',
        choices=TIPO_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
        initial='saldo_nao_previsto'
    )
    
    descricao = forms.CharField(
        label='Descrição',
        max_length=255,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ex: Pagamento de compras'
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
            'tipopgto',
            'descricao',
            Row(
                Column('data_primeira_parcela', css_class='form-group col-md-6 mb-0'),
                Column('num_parcelas', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            'observacao',
            Div(
                Submit('submit', 'Salvar', css_class='btn btn-success'),
                Button('cancel', 'Cancelar', css_class='btn btn-outline-danger', onclick="window.history.back()"),
                css_class='text-right mt-4'
            )
        )
