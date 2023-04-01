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

        codcliente = self.instance.codcliente

        if codcliente:
            self.fields["codcliente"].widget.attrs = {
                "readonly": "readonly",
                "size": "10",
                "class": "form-control",
            }
        else:
            self.fields["codcliente"].widget = forms.HiddenInput()

        # self.fields["codcliente"].widget.attrs["size"] = "10"
        # self.fields["codcliente"].widget.attrs["readonly"] = "readonly"
        self.fields["nomecliente"].widget.attrs = {
            "size": "47",
            "class": "form-control",
        }
        self.fields["telefone"].widget.attrs = {
            "size": "20",
            "class": "form-control",
        }
        self.fields["observacao"].widget = forms.Textarea(
            attrs={"cols": 50, "rows": 4, "class": "form-control"}
        )
