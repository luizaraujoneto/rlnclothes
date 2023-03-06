from django.db import models

from pedidos.models import Pedidos


# Create your models here.
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
