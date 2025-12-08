import django_tables2 as tables
from django.utils.html import format_html
from .models import NotasFiscais, ContasPagar

class NotasFiscaisTable(tables.Table):
    codnotafiscal = tables.Column(
        verbose_name="Cód", attrs={"th": {"class": "text-center"}}
    )
    numeronotafiscal = tables.Column(verbose_name="Nota Fiscal")
    fornecedor = tables.Column(verbose_name="Fornecedor")
    datanotafiscal = tables.Column(verbose_name="Data", localize=True)
    valornotafiscal = tables.Column(
        verbose_name="Valor", attrs={"th": {"class": "text-right"}}
    )
    observacao = tables.Column(
        verbose_name="Obs.", attrs={"th": {"class": "text-center"}}, default=""
    )
    formapagamento = tables.Column(verbose_name="Forma de Pagamento")

    def render_valornotafiscal(self, value):
        return "R$ {:0.2f}".format(value).replace(".", ",")

    def render_datanotafiscal(self, value):
        return value.strftime("%d/%m/%Y")

    def render_observacao(self, value):
        html = "&nbsp;<span class='text-info' title='{}'><i class='bi bi-journal-text'></i>&nbsp; </span>"

        return format_html(html, value)

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

class ContasPagarTable(tables.Table):
    class Meta:
        model = ContasPagar
