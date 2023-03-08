from django.db import models

from clientes.models import Cliente
from pedidos.models import Produtos

# Create your models here.


class Vendas(models.Model):
    codvenda = models.IntegerField(
        db_column="codvenda", blank=True, null=False, primary_key=True
    )

    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.PROTECT,
        db_column="codcliente",
        to_field="codcliente",
        blank=True,
        null=True,
    )

    datavenda = models.DateTimeField(db_column="datavenda", blank=True, null=True)
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
