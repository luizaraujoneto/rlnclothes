from django.db import models
import django_tables2 as tables


# Create your models here.
class Pedido(models.Model):
    codpedido = models.IntegerField(
        db_column="codpedido", blank=True, null=False, primary_key=True
    )  # Field name made lowercase.
    numeropedido = models.CharField(
        db_column="numeropedido", max_length=255, blank=True, null=True
    )  # Field name made lowercase.
    codfornecedor = models.IntegerField(
        db_column="codfornecedor", blank=True, null=True
    )  # Field name made lowercase.
    codnotafiscal = models.IntegerField(
        db_column="codnotafiscal", blank=True, null=True
    )  # Field name made lowercase.
    datapedido = models.DateField(
        db_column="datapedido", blank=True, null=True
    )  # Field name made lowercase.
    valorpedido = models.DecimalField(
        db_column="valorpedido", blank=True, null=True, max_digits=15, decimal_places=2
    )  # Field name made lowercase.
    observacao = models.CharField(
        db_column="observacao", max_length=255, blank=True, null=True
    )  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = "pedidos"


class PedidoTable(tables.Table):
    class Meta:
        model = Pedido
