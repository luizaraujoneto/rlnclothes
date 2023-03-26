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


class ProdutosForm(forms.ModelForm):
    class Meta:
        model = Produtos
        fields = "__all__"
        labels = {
            "codproduto": "Cód. Produto",
            "codprodutofornecedor": "Cód. Fornecedor",
            "referencia": "Referência",
            "descricao": "Descrição",
            "valorcusto": "Valor Custo",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        codproduto = self.instance.codproduto
        if codproduto:
            self.fields["codproduto"].widget.attrs = {
                "readonly": "readonly",
                "width": "50",
            }
        else:
            self.fields["codproduto"].widget = forms.HiddenInput()
        self.fields["pedido"].widget = forms.HiddenInput()
        self.fields["descricao"].widget.attrs["size"] = "50"
