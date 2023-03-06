from django.db import models
import django_tables2 as tables

from fornecedores.models import Fornecedores
from notasfiscais.models import NotasFiscais


# Create your models here.
class Pedidos(models.Model):
    codpedido = models.AutoField(db_column="codpedido", primary_key=True)
    numeropedido = models.CharField(
        db_column="numeropedido", max_length=255, blank=True, null=True
    )
    fornecedor = models.ForeignKey(
        Fornecedores,
        on_delete=models.PROTECT,
        db_column="codfornecedor",
        to_field="codfornecedor",
        blank=True,
        null=True,
    )

    #    codnotafiscal = models.IntegerField( db_column="codnotafiscal", blank=True, null=True  )

    notafiscal = models.ForeignKey(
        NotasFiscais,
        on_delete=models.PROTECT,
        db_column="codnotafiscal",
        to_field="codnotafiscal",
        blank=True,
        null=True,
    )

    datapedido = models.DateField(db_column="datapedido", blank=True, null=True)
    valorpedido = models.DecimalField(
        db_column="valorpedido", blank=True, null=True, max_digits=15, decimal_places=2
    )
    observacao = models.CharField(
        db_column="observacao", max_length=255, blank=True, null=True
    )

    def __str__(self):
        return self.numeropedido[:20]

    class Meta:
        managed = False
        db_table = "pedidos"


class PedidoTable(tables.Table):
    class Meta:
        model = Pedidos


class Produtos(models.Model):
    codproduto = models.IntegerField(
        db_column="codproduto", blank=True, null=False, primary_key=True
    )
    # codpedido = models.IntegerField(db_column="codpedido", blank=True, null=True)

    pedido = models.ForeignKey(
        Pedidos,
        on_delete=models.PROTECT,
        db_column="codpedido",
        to_field="codpedido",
        blank=True,
        null=True,
    )

    codprodutofornecedor = models.CharField(
        db_column="codprodutofornecedor", max_length=255, blank=True, null=True
    )
    referencia = models.CharField(
        db_column="referencia", max_length=255, blank=True, null=True
    )
    descricao = models.CharField(
        db_column="descricao", max_length=255, blank=True, null=True
    )
    valorcusto = models.FloatField(db_column="valorcusto", blank=True, null=True)

    class Meta:
        managed = False
        db_table = "produtos"
