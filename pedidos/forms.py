from django import forms

from fornecedores.models import Fornecedores
from notasfiscais.models import NotasFiscais
from pedidos.models import Pedido


class PedidosForm(forms.Form):
    codpedido = forms.IntegerField(label="Código", disabled=True)
    numeropedido = forms.CharField(label="Número")
    # codfornecedor = forms.IntegerField(label="Cód. Fornecedor")
    fornecedor = forms.ModelChoiceField(
        queryset=Fornecedores.objects.all(),
        label="Fornecedor",
        to_field_name="codfornecedor",
    )
    # codnotafiscal = forms.IntegerField(label="Cód. Nota Fiscal")
    notafiscal = forms.ModelChoiceField(
        queryset=NotasFiscais.objects.all(), label="Nota Fiscal"
    )
    datapedido = forms.DateField(
        label="Data", widget=forms.DateInput(attrs={"type": "date"})
    )
    valorpedido = forms.DecimalField(
        label="Valor", widget=forms.TextInput(attrs={"type": "number", "step": "0.01"})
    )  # forms.FloatField(label="Valor")
    observacao = forms.CharField(
        label="Observacao", widget=forms.Textarea(attrs={"cols": 50, "rows": 4})
    )

    class Meta:
        model = Pedido
        fields = [
            "codigopedido",
            "numeropedido",
            "fornecedor",
            "codnotafiscal",
            "datapedido",
            "valorpedido",
            "observacao",
        ]
