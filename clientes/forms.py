from django import forms
from clientes.models import Clientes


class ClientesForm(forms.ModelForm):
    class Meta:
        model = Clientes
        fields = ["codcliente", "nomecliente", "telefone", "observacao"]
        labels = {
            "codcliente": "Código",
            "nomecliente": "Nome Cliente",
            "telefone": "Telefone",
            "observacao": "Observação",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["codcliente"].widget.attrs["size"] = "10"
        self.fields["codcliente"].widget.attrs["readonly"] = "readonly"
        self.fields["nomecliente"].widget.attrs["size"] = "47"
        self.fields["observacao"].widget = forms.Textarea(attrs={"cols": 50, "rows": 4})
