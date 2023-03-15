from django.db import models
import django_tables2 as tables
from django.db.models.functions import Concat
from django.db.models import Value

# from clientes.models import Clientes

from pedidos.models import Produtos

# Create your models here.

# Vendas - codvenda, codcliente, datavenda, codproduto, valorvenda, observacao


class Vendas(models.Model):
    codvenda = models.IntegerField(
        db_column="codvenda", blank=True, null=False, primary_key=True
    )

    cliente = models.ForeignKey(
        "clientes.Clientes",
        on_delete=models.PROTECT,
        db_column="codcliente",
        to_field="codcliente",
        # to_field_name=Concat("codcliente", Value(":"), "nomecliente"),
        blank=True,
        null=True,
    )

    datavenda = models.DateField(db_column="datavenda", blank=True, null=True)

    produto = models.OneToOneField(
        Produtos,
        on_delete=models.PROTECT,
        db_column="codproduto",
        to_field="codproduto",
        # to_field_name=Concat("referencia", Value(":"), "descricao"),
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
        db_table = "vendas"

    def __str__(self):
        return self.codvenda

    def save(self, *args, **kwargs):
        if not self.codvenda:
            max = Vendas.objects.aggregate(models.Max("codvenda"))["codvenda__max"]
            self.codvenda = max + 1
        super().save(*args, **kwargs)


class VendaTable(tables.Table):
    class Meta:
        model = Vendas
