from django.db import models
from django.utils.html import format_html
# import django_tables2 as tables

from fornecedores.models import Fornecedores
from notasfiscais.models import NotasFiscais


# Create your models here.
class Pedidos(models.Model):
    """
    Modelo representativo de Pedidos.
    Gerencia pedidos de compra e devolução junto a fornecedores/notas fiscais.
    """
    codpedido = models.IntegerField(
        db_column="codpedido", blank=True, null=False, primary_key=True
    )
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

    TIPOS_PEDIDO = [("C", "Compra"), ("D", "Devolução")]

    tipopedido = models.CharField(
        db_column="tipo_pedido",
        max_length=1,
        blank=False,
        null=False,
        choices=TIPOS_PEDIDO,
    )

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
        db_column="valorpedido",
        blank=False,
        null=False,
        max_digits=10,
        decimal_places=2,
    )
    observacao = models.CharField(
        db_column="observacao", max_length=255, blank=True, null=True
    )

    def save(self, *args, **kwargs) -> None:
        if not self.codpedido:
            max = Pedidos.objects.aggregate(models.Max("codpedido"))["codpedido__max"] or 0
            self.codpedido = max + 1
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.numeropedido[:20]

    class Meta:
        managed = False
        db_table = "pedidos"


# PedidoTable moved to tables.py


class Produtos(models.Model):
    """
    Modelo representativo de Produtos.
    Armazena itens individuais associados a um pedido.
    """
    codproduto = models.IntegerField(
        db_column="codproduto", blank=True, null=False, primary_key=True
    )

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
    valorcusto = models.DecimalField(
        db_column="valorcusto", blank=True, null=True, max_digits=10, decimal_places=2
    )

    class Meta:
        managed = False
        db_table = "produtos"

    def save(self, *args, **kwargs) -> None:
        if not self.codproduto:
            max = Produtos.objects.aggregate(models.Max("codproduto"))[
                "codproduto__max"
            ] or 0
            self.codproduto = max + 1
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.descricao[:20] + " [Ref.:" + (self.referencia or "     ") + "]"


class Devolucoes(models.Model):
    """
    Modelo representativo de Devoluções.
    Registra a devolução de produtos de um pedido específico.
    """
    coddevolucao = models.IntegerField(
        db_column="coddevolucao", blank=True, null=False, primary_key=True
    )

    pedido = models.ForeignKey(
        Pedidos,
        on_delete=models.PROTECT,
        db_column="codpedido",
        to_field="codpedido",
        blank=False,
        null=False,
    )

    produto = models.ForeignKey(
        Produtos,
        on_delete=models.PROTECT,
        db_column="codproduto",
        to_field="codproduto",
        blank=False,
        null=False,
    )

    class Meta:
        managed = False
        db_table = "devolucoes"

    def save(self, *args, **kwargs) -> None:
        if not self.coddevolucao:
            max = (
                Devolucoes.objects.aggregate(models.Max("coddevolucao"))[
                    "coddevolucao__max"
                ]
                or 0
            )
            self.coddevolucao = max + 1
        super().save(*args, **kwargs)
