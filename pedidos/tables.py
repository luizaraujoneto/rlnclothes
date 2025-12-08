import django_tables2 as tables
from django.utils.html import format_html
from .models import Pedidos

class PedidoTable(tables.Table):
    codpedido = tables.Column(
        verbose_name="Cód", attrs={"th": {"class": "text-center"}}
    )
    numeropedido = tables.Column(verbose_name="Pedido")
    fornecedor = tables.Column(verbose_name="Fornecedor")
    notafiscal = tables.Column(verbose_name="Nota Fiscal")
    datapedido = tables.Column(verbose_name="Data", localize=True)
    valorpedido = tables.Column(
        verbose_name="Valor", attrs={"th": {"class": "text-right"}}
    )
    observacao = tables.Column(
        verbose_name="Obs.", attrs={"th": {"class": "text-center"}}, default=""
    )

    def render_valorpedido(self, value):
        return "R$ {:0.2f}".format(value).replace(".", ",")

    def render_datapedido(self, value):
        return value.strftime("%d/%m/%Y")

    def render_observacao(self, value):
        html = "&nbsp;<span class='text-info' title='{}'><i class='bi bi-journal-text'></i>&nbsp; </span>"

        return format_html(html, value)

    class Meta:
        model = Pedidos
