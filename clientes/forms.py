from django import forms
from clientes.models import Clientes

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Row, Column, Submit, Button, ButtonHolder


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

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.label_class = "fw-bold"  # aplica negrito aos rótulos (opcional)
        self.helper.form_show_labels = True

        codcliente = self.instance.codcliente

        if codcliente:
            self.fields["codcliente"].widget.attrs = {
                "readonly": "readonly",
                "class": "form-control-plaintext",
            }
        else:
            self.fields["codcliente"].widget = forms.HiddenInput()

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
