from django import forms

from fornecedores.models import Fornecedores
from notasfiscais.models import NotasFiscais
from pedidos.models import Pedidos, Produtos


class PedidosForm(forms.ModelForm):
    class Meta:
        model = Pedidos
        fields = [
            "codpedido",
            "numeropedido",
            "fornecedor",
            "notafiscal",
            "datapedido",
            "valorpedido",
            "observacao",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["codpedido"].widget.attrs["readonly"] = "readonly"
        self.fields["datapedido"].widget = forms.DateInput(attrs={"type": "date"})
        self.fields["observacao"].widget = forms.Textarea(attrs={"cols": 50, "rows": 4})


"""    
    codpedido = forms.IntegerField(label="Código")
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
"""


class ProdutosForm(forms.ModelForm):
    class Meta:
        model = Produtos
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["codproduto"].widget.attrs["readonly"] = "readonly"
        self.fields["pedido"].widget = forms.HiddenInput()
        self.fields["descricao"].widget.attrs["width"] = "50"
