from django.db import models
import django_tables2 as tables


# from clientes.models import Clientes

from pedidos.models import Produtos

# Create your models here.


class Vendas(models.Model):
    codvenda = models.IntegerField(
        db_column="codvenda", blank=True, null=False, primary_key=True
    )

    cliente = models.ForeignKey(
        "clientes.Clientes",
        on_delete=models.PROTECT,
        db_column="codcliente",
        to_field="codcliente",
        blank=True,
        null=True,
    )

    datavenda = models.DateField(db_column="datavenda", blank=True, null=True)
    valorvenda = models.DecimalField(
        db_column="valorvenda", blank=True, null=True, max_digits=6, decimal_places=2
    )
    observacao = models.CharField(
        db_column="observacao", max_length=255, blank=True, null=True
    )
    condicaopagamento = models.CharField(
        db_column="condicaopagamento", max_length=255, blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "vendas"


class VendaTable(tables.Table):
    class Meta:
        model = Vendas


class ItemVenda(models.Model):
    coditemvenda = models.IntegerField(
        db_column="coditemvenda", blank=True, null=False, primary_key=True
    )

    venda = models.ForeignKey(
        Vendas,
        on_delete=models.PROTECT,
        db_column="codvenda",
        to_field="codvenda",
        blank=True,
        null=True,
    )

    produto = models.OneToOneField(
        Produtos,
        on_delete=models.PROTECT,
        db_column="codproduto",
        to_field="codproduto",
        blank=True,
        null=True,
    )

    valorvenda = models.DecimalField(
        db_column="valorvenda", blank=True, null=True, max_digits=6, decimal_places=2
    )
    observacao = models.CharField(
        db_column="observacao", max_length=255, blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "itemvenda"


class ContasReceber(models.Model):
    codcontareceber = models.IntegerField(
        db_column="codcontareceber", blank=True, null=False, primary_key=True
    )

    venda = models.ForeignKey(
        Vendas,
        on_delete=models.PROTECT,
        db_column="codvenda",
        to_field="codvenda",
        blank=True,
        null=True,
    )
    datavencimento = models.DateField(db_column="datavencimento", blank=True, null=True)
    valorparcela = models.DecimalField(
        db_column="valorparcela", blank=True, null=True, max_digits=6, decimal_places=2
    )
    formapagamento = models.CharField(
        db_column="formapagamento", max_length=255, blank=True, null=True
    )
    parcela = models.CharField(
        db_column="parcela", max_length=255, blank=True, null=True
    )
    datapagamento = models.DateField(db_column="datapagamento", blank=True, null=True)
    valorpago = models.DecimalField(
        db_column="valorpago", blank=True, null=True, max_digits=6, decimal_places=2
    )
    observacao = models.CharField(
        db_column="observacao", max_length=255, blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "contasreceber"
