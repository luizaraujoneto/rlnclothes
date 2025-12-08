from django.db import models
from typing import Dict, List, Any
from django.db.models.functions import Cast
from django.db.models import Sum

# import django_tables2 as tables

from decimal import Decimal
from django.utils.html import format_html
from django.utils import timezone
import pytz

from math import isclose

from vendas.models import Vendas
from pagamentos.models import Pagamentos

# Create your models here.


class Clientes(models.Model):
    """
    Modelo representativo de Clientes.
    Gerencia informações pessoais e financeiras básicas dos clientes.
    """
    codcliente = models.IntegerField(
        db_column="codcliente", blank=True, null=False, primary_key=True
    )
    nomecliente = models.CharField(
        db_column="nomecliente", max_length=100, blank=False, null=False
    )
    telefone = models.CharField(
        db_column="telefone", max_length=50, blank=True, null=True
    )
    observacao = models.CharField(
        db_column="observacao", max_length=255, blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "clientes"

    def __str__(self):
        return self.nomecliente[:50]

    def save(self, *args, **kwargs) -> None:
        if not self.codcliente:
            max = Clientes.objects.aggregate(models.Max("codcliente"))[
                "codcliente__max"
            ] or 0
            self.codcliente = max + 1
        super().save(*args, **kwargs)

    def totalvendas(self) -> Decimal:
        return Decimal(
            Vendas.objects.filter(cliente=self).aggregate(
                totalvendas=models.Sum("valorvenda")
            )["totalvendas"]
            or Decimal("0.00")
        )

    def totalpagamentos(self) -> Decimal:
        return Decimal(
            Pagamentos.objects.filter(cliente=self)
            .filter(tipopagamento="C")
            .aggregate(totalpagamentoconfirmado=models.Sum("valorpagamento"))[
                "totalpagamentoconfirmado"
            ]
            or Decimal("0.00")
        )

    def totalcontasareceber(self) -> Decimal:
        return Decimal(
            Pagamentos.objects.filter(cliente=self)
            .filter(tipopagamento="P")
            .aggregate(totalcontasareceber=models.Sum("valorpagamento"))[
                "totalcontasareceber"
            ]
            or Decimal("0.00")
        )

    def saldocliente(self) -> Decimal:
        vendas = Decimal( self.totalvendas() )
        pagamentos = Decimal( self.totalpagamentos() )

        return round(vendas - pagamentos, 2)

    def possuiParcelaEmAtraso(self) -> bool:
        atraso = False

        parcelas = Pagamentos.objects.filter(cliente=self).filter(tipopagamento="P")

        for p in parcelas:
            if p.datapagamento < timezone.localdate():
                atraso = True

        return atraso

    def historico(self) -> Dict[str, Any]:
        colunas = []
        for f in HistoricoCliente()._meta.get_fields():
            colunas.append(f.name)

        dados = []
        saldo = Decimal("0.00")
        for h in HistoricoCliente.objects.filter(cliente=self).values():
            linha = h
            valor = Decimal(h["valor"])
            if h["tipooperacao"] == "V":
                saldo = saldo - valor
            else:
                saldo = saldo + valor
            linha["saldo"] = saldo

            dados.append(linha)

        table = {"colunas": colunas, "dados": dados, "valor": saldo}

        return table

    def vendas(self) -> Dict[str, Any]:
        colunas = ["codvenda", "datavenda", "descricao", "valorvenda", "observacao"]

        dados = (
            HistoricoCliente.objects.filter(cliente=self)
            .filter(tipooperacao="V")
            .order_by("data")
            .values_list("codoperacao", "data", "descricao", "valor", "observacao")
        )

        valor = Decimal("0.00")
        for v in dados:
            valor = valor + Decimal(v[3])

        table = {"colunas": colunas, "dados": dados, "valor": valor}

        return table

    def pagamentos(self, tipo: str) -> Dict[str, Any]:
        if tipo == "E":  # Pagamentos "E"fetivados
            colunas = ["Id", "Data Pgto.", "Forma Pgto.", "Valor Pago", "Observação"]

            dados = (
                HistoricoCliente.objects.filter(cliente=self)
                .filter(tipooperacao="P")
                .order_by("data")
                .values_list("codoperacao", "data", "descricao", "valor", "observacao")
            )

            valor = Decimal("0.00")
            for v in dados:
                valor = valor + Decimal(v[3]) or Decimal("0.00")

        elif tipo == "P":  # Pagamentos "P"revistos
            colunas = [
                "Id",
                "Descrição",
                "Data Vencimento",
                "Valor Previsto",
                "Observação",
            ]

            dados = (
                Pagamentos.objects.filter(cliente=self)
                .filter(tipopagamento="P")
                .select_related("venda")
                .order_by("datapagamento")
                .values_list(
                    "codpagamento",
                    "formapagamento",
                    "datapagamento",
                    "valorpagamento",
                    "observacao",
                )
            )

            valor = Decimal("0.00")
            for v in dados:
                valor = valor + Decimal(v[3])

        table = {"colunas": colunas, "dados": dados, "valor": valor}

        return table


# ClienteTable moved to tables.py


# cliente, tipooperacao, codoperacao, data, descricao, valor, observacao


class HistoricoCliente(models.Model):
    """
    Modelo de visualização do histórico do cliente.
    Consolida operações de vendas e pagamentos para exibição.
    Esta é uma tabela gerenciada via view no banco de dados.
    """
    cliente = models.ForeignKey(
        Clientes,
        on_delete=models.DO_NOTHING,
        db_column="codcliente",
        to_field="codcliente",
        blank=True,
        null=True,
    )

    tipooperacao = models.CharField(
        db_column="tipooperacao", max_length=1, blank=True, null=True
    )
    codoperacao = models.IntegerField(db_column="codoperacao", blank=True, null=True)
    data = models.DateField(db_column="data", blank=True, null=True)
    descricao = models.CharField(
        db_column="descricao", max_length=255, blank=True, null=True
    )
    valor = models.DecimalField(
        db_column="valorvenda", blank=True, null=True, max_digits=10, decimal_places=2
    )
    observacao = models.CharField(
        db_column="observacao", max_length=255, blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "vw_historicocliente"
        ordering = ["data", "-tipooperacao"]
