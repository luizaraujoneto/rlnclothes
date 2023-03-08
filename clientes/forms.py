from django import forms
from clientes.models import Clientes


class ClientesForm(forms.ModelForm):
    class Meta:
        model = Clientes
        fields = ["codcliente", "nomecliente", "telefone"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["codcliente"].widget.attrs["readonly"] = "readonly"
