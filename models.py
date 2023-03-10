# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Clientes(models.Model):
    codcliente = models.IntegerField(
        db_column="CodCliente", blank=True, null=True
    )  # Field name made lowercase.
    cliente = models.CharField(
        db_column="Cliente", max_length=255, blank=True, null=True
    )  # Field name made lowercase.
    telefone = models.CharField(
        db_column="Telefone", max_length=255, blank=True, null=True
    )  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = "Clientes"


class Contaspagar(models.Model):
    codcontapagar = models.IntegerField(
        db_column="CodContaPagar", blank=True, null=True
    )  # Field name made lowercase.
    codnotafiscal = models.IntegerField(
        db_column="CodNotaFiscal", blank=True, null=True
    )  # Field name made lowercase.
    parcela = models.CharField(
        db_column="Parcela", max_length=255, blank=True, null=True
    )  # Field name made lowercase.
    datavencimento = models.DateTimeField(
        db_column="DataVencimento", blank=True, null=True
    )  # Field name made lowercase.
    valor = models.FloatField(
        db_column="Valor", blank=True, null=True
    )  # Field name made lowercase.
    datapagamento = models.DateTimeField(
        db_column="DataPagamento", blank=True, null=True
    )  # Field name made lowercase.
    formapagamento = models.CharField(
        db_column="FormaPagamento", max_length=255, blank=True, null=True
    )  # Field name made lowercase.
    observacao = models.CharField(
        db_column="Observacao", max_length=255, blank=True, null=True
    )  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = "ContasPagar"


class Contasreceber(models.Model):
    codcontareceber = models.IntegerField(
        db_column="CodContaReceber", blank=True, null=True
    )  # Field name made lowercase.
    codvenda = models.IntegerField(
        db_column="CodVenda", blank=True, null=True
    )  # Field name made lowercase.
    datavencimento = models.DateTimeField(
        db_column="DataVencimento", blank=True, null=True
    )  # Field name made lowercase.
    valorparcela = models.FloatField(
        db_column="ValorParcela", blank=True, null=True
    )  # Field name made lowercase.
    formapagamento = models.CharField(
        db_column="FormaPagamento", max_length=255, blank=True, null=True
    )  # Field name made lowercase.
    parcela = models.CharField(
        db_column="Parcela", max_length=255, blank=True, null=True
    )  # Field name made lowercase.
    datapagamento = models.DateTimeField(
        db_column="DataPagamento", blank=True, null=True
    )  # Field name made lowercase.
    valorpago = models.FloatField(
        db_column="ValorPago", blank=True, null=True
    )  # Field name made lowercase.
    observacao = models.CharField(
        db_column="Observacao", max_length=255, blank=True, null=True
    )  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = "ContasReceber"


class Fornecedores(models.Model):
    codfornecedor = models.IntegerField(
        db_column="CodFornecedor", blank=True, null=True
    )  # Field name made lowercase.
    fornecedor = models.CharField(
        db_column="Fornecedor", max_length=255, blank=True, null=True
    )  # Field name made lowercase.
    telefone = models.CharField(
        db_column="Telefone", max_length=255, blank=True, null=True
    )  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = "Fornecedores"


class Itemvenda(models.Model):
    coditemvenda = models.IntegerField(
        db_column="CodItemVenda", blank=True, null=True
    )  # Field name made lowercase.
    codvenda = models.IntegerField(
        db_column="CodVenda", blank=True, null=True
    )  # Field name made lowercase.
    codproduto = models.IntegerField(
        db_column="CodProduto", blank=True, null=True
    )  # Field name made lowercase.
    valorvenda = models.FloatField(
        db_column="ValorVenda", blank=True, null=True
    )  # Field name made lowercase.
    observacao = models.CharField(
        db_column="Observacao", max_length=255, blank=True, null=True
    )  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = "ItemVenda"


class Notasfiscais(models.Model):
    codnotafiscal = models.IntegerField(
        db_column="CodNotaFiscal", blank=True, null=True
    )  # Field name made lowercase.
    numeronotafiscal = models.CharField(
        db_column="NumeroNotaFiscal", max_length=255, blank=True, null=True
    )  # Field name made lowercase.
    codfornecedor = models.IntegerField(
        db_column="CodFornecedor", blank=True, null=True
    )  # Field name made lowercase.
    datanotafiscal = models.DateTimeField(
        db_column="DataNotaFiscal", blank=True, null=True
    )  # Field name made lowercase.
    valornotafiscal = models.FloatField(
        db_column="ValorNotaFiscal", blank=True, null=True
    )  # Field name made lowercase.
    observacao = models.CharField(
        db_column="Observacao", max_length=255, blank=True, null=True
    )  # Field name made lowercase.
    formapagamento = models.CharField(
        db_column="FormaPagamento", max_length=255, blank=True, null=True
    )  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = "NotasFiscais"


class Pedidos(models.Model):
    codpedido = models.IntegerField(
        db_column="CodPedido", blank=True, null=True
    )  # Field name made lowercase.
    numeropedido = models.CharField(
        db_column="NumeroPedido", max_length=255, blank=True, null=True
    )  # Field name made lowercase.
    codfornecedor = models.IntegerField(
        db_column="CodFornecedor", blank=True, null=True
    )  # Field name made lowercase.
    codnotafiscal = models.IntegerField(
        db_column="CodNotaFiscal", blank=True, null=True
    )  # Field name made lowercase.
    datapedido = models.DateTimeField(
        db_column="DataPedido", blank=True, null=True
    )  # Field name made lowercase.
    valorpedido = models.FloatField(
        db_column="ValorPedido", blank=True, null=True
    )  # Field name made lowercase.
    observacao = models.CharField(
        db_column="Observacao", max_length=255, blank=True, null=True
    )  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = "Pedidos"


class Produtos(models.Model):
    codproduto = models.IntegerField(
        db_column="CodProduto", blank=True, null=True
    )  # Field name made lowercase.
    codpedido = models.IntegerField(
        db_column="CodPedido", blank=True, null=True
    )  # Field name made lowercase.
    codprodutofornecedor = models.CharField(
        db_column="CodProdutoFornecedor", max_length=255, blank=True, null=True
    )  # Field name made lowercase.
    referencia = models.CharField(
        db_column="Referencia", max_length=255, blank=True, null=True
    )  # Field name made lowercase.
    descricao = models.CharField(
        db_column="Descricao", max_length=255, blank=True, null=True
    )  # Field name made lowercase.
    valorcusto = models.FloatField(
        db_column="ValorCusto", blank=True, null=True
    )  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = "Produtos"


class Vendas(models.Model):
    codvenda = models.IntegerField(
        db_column="CodVenda", blank=True, null=True
    )  # Field name made lowercase.
    codcliente = models.IntegerField(
        db_column="CodCliente", blank=True, null=True
    )  # Field name made lowercase.
    datavenda = models.DateTimeField(
        db_column="DataVenda", blank=True, null=True
    )  # Field name made lowercase.
    valorvenda = models.FloatField(
        db_column="ValorVenda", blank=True, null=True
    )  # Field name made lowercase.
    observacao = models.CharField(
        db_column="Observacao", max_length=255, blank=True, null=True
    )  # Field name made lowercase.
    condicaopagamento = models.CharField(
        db_column="CondicaoPagamento", max_length=255, blank=True, null=True
    )  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = "Vendas"
