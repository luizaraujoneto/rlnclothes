from django.db import models

import django_tables2 as tables

from vendas.models import Vendas, ContasReceber

# Create your models here.


class Clientes(models.Model):
    codcliente = models.IntegerField(
        db_column="codcliente", blank=True, null=False, primary_key=True
    )
    nomecliente = models.CharField(
        db_column="nomecliente", max_length=255, blank=True, null=True
    )
    telefone = models.CharField(
        db_column="telefone", max_length=255, blank=True, null=True
    )

    class Meta:
        db_table = "clientes"

    def saldocliente(self):
        vendas = (
            Vendas.objects.filter(cliente=self).aggregate(
                vendas=models.Sum("valorvenda")
            )["vendas"]
            or 0
        )

        codvenda_list = []
        for v in Vendas.objects.filter(cliente=self):
            codvenda_list.append(v.codvenda)

        recebido = (
            ContasReceber.objects.filter(venda__in=codvenda_list).aggregate(
                recebido=models.Sum("valorpago")
            )["recebido"]
            or 0
        )

        return float(vendas - recebido)

    def __str__(self):
        return self.nomecliente[:50]

    def save(self, *args, **kwargs):
        if not self.codcliente:
            max = Clientes.objects.aggregate(models.Max("codcliente"))[
                "codcliente__max"
            ]
            self.codcliente = max + 1
        super().save(*args, **kwargs)


class ClienteTable(tables.Table):
    class Meta:
        model = Clientes


class HistoricoCliente(models.Model):
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
        db_column="valor", blank=True, null=True, max_digits=6, decimal_places=2
    )
    observacao = models.CharField(
        db_column="observacao", max_length=255, blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "vw_historicocliente"
        ordering = ["data", "-tipooperacao"]
