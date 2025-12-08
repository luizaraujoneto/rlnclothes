from decimal import Decimal
from math import isclose
from django.utils.html import format_html
import django_tables2 as tables
from .models import Clientes

class ClienteTable(tables.Table):
    codcliente = tables.Column(
        verbose_name="Cód", attrs={"th": {"class": "text-center"}}
    )
    nomecliente = tables.Column(verbose_name="Nome", orderable="True")
    telefone = tables.Column(verbose_name="Telefone")
    observacao = tables.Column(
        verbose_name="Obs.", attrs={"th": {"class": "text-center"}}, default=""
    )
    saldo = tables.Column(
        verbose_name="Saldo", empty_values=(), attrs={"th": {"class": "text-right"}}
    )

    def render_codcliente(self, record):
        cliente = record
        msg1 = ""
        msg2 = ""

        # if round( or 0, 2) != round(
        #     cliente.totalcontasareceber() or 0, 2
        # ):
        if not isclose(cliente.saldocliente(), cliente.totalcontasareceber()):
            msg1 = "Inconsistência entre Saldo e Previsão de Pagamentos."

        if cliente.possuiParcelaEmAtraso():
            msg2 = "Cliente posui parcela em atraso."

        html = "&nbsp;<span class='text-danger small' title='{}\n{}'><i class='bi bi-patch-exclamation'></i>&nbsp; </span>"

        if msg1 != "" or msg2 != "":
            return format_html(str(cliente.codcliente) + html, msg1, msg2)
        else:
            return cliente.codcliente

    def render_saldo(self, record):
        saldo = Decimal(record.saldocliente() or 0)
        return "R$ {:0.2f}".format(saldo).replace(".", ",")

    def render_observacao(self, value):
        html = "&nbsp;<span class='text-info' title='{}'><i class='bi bi-journal-text'></i>&nbsp; </span>"

        return format_html(html, value)

    class Meta:
        model = Clientes
        fields = [
            "codcliente",
            "nomecliente",
            "telefone",
            "observacao",
            "saldo",
        ]
