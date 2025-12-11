from django.db import models
from django.db.models import Sum
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

    @staticmethod
    def atualizar_valor_pedido(pedido):
        """Atualiza o valor total do pedido com base na soma dos produtos associados.
        
        Para pedidos de compra (tipo "C"), soma os produtos do modelo Produtos.
        Para pedidos de devolução (tipo "D"), soma os produtos do modelo Devolucoes.
        
        Args:
            pedido: Instância de Pedidos ou codpedido (int)
        """
        if isinstance(pedido, int):
            codpedido = pedido
            pedido_obj = Pedidos.objects.get(codpedido=codpedido)
        else:
            codpedido = pedido.codpedido
            pedido_obj = pedido
        
        # Verifica o tipo do pedido para determinar de onde buscar os produtos
        if pedido_obj.tipopedido == 'C':
            # Pedido de Compra: calcula o total baseado nos produtos do pedido
            total = Produtos.objects.filter(pedido__codpedido=codpedido).aggregate(
                total=Sum('valorcusto')
            )['total'] or 0
        elif pedido_obj.tipopedido == 'D':
            # Pedido de Devolução: calcula o total baseado nas devoluções
            total = Devolucoes.objects.filter(pedido__codpedido=codpedido).aggregate(
                total=Sum('produto__valorcusto')
            )['total'] or 0
        else:
            # Tipo de pedido desconhecido, define total como 0
            total = 0
        
        # Atualiza o valor do pedido
        Pedidos.objects.filter(codpedido=codpedido).update(valorpedido=total)

    def save(self, *args, **kwargs) -> None:
        # Assign a new primary key if this is a new record
        if not self.codpedido:
            max = Pedidos.objects.aggregate(models.Max("codpedido"))["codpedido__max"] or 0
            self.codpedido = max + 1
        # Ensure valorpedido has a default before initial save
        if not self.valorpedido:
            self.valorpedido = 0
        # Save the order first so that related Produtos can reference it
        super().save(*args, **kwargs)
        # Recalculate order total
        Pedidos.atualizar_valor_pedido(self)

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
            max = Produtos.objects.aggregate(models.Max("codproduto"))["codproduto__max"] or 0
            self.codproduto = max + 1
        super().save(*args, **kwargs)
        # After saving the product, update the related order's total value
        if self.pedido:
            Pedidos.atualizar_valor_pedido(self.pedido)

    def delete(self, *args, **kwargs) -> None:
        """Delete the product and recalculate the order total.
        """
        # Preserve reference to the related order before deletion
        related_pedido = self.pedido
        super().delete(*args, **kwargs)
        if related_pedido:
            Pedidos.atualizar_valor_pedido(related_pedido)

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
        # After saving a devolucao, recalculate the order total
        if self.pedido:
            Pedidos.atualizar_valor_pedido(self.pedido)
    
    def delete(self, *args, **kwargs) -> None:
        """Delete the devolucao and recalculate the order total."""
        # Preserve reference to the related order before deletion
        related_pedido = self.pedido
        super().delete(*args, **kwargs)
        if related_pedido:
            Pedidos.atualizar_valor_pedido(related_pedido)
