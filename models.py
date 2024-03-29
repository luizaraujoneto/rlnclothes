from django.db import models


class Clientes(models.Model):
    codcliente = models.IntegerField(db_column="CodCliente", blank=True, null=True)
    cliente = models.CharField(
        db_column="Cliente", max_length=255, blank=True, null=True
    )
    telefone = models.CharField(
        db_column="Telefone", max_length=255, blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "Clientes"


class Contaspagar(models.Model):
    codcontapagar = models.IntegerField(
        db_column="CodContaPagar", blank=True, null=True
    )
    codnotafiscal = models.IntegerField(
        db_column="CodNotaFiscal", blank=True, null=True
    )
    parcela = models.CharField(
        db_column="Parcela", max_length=255, blank=True, null=True
    )
    datavencimento = models.DateTimeField(
        db_column="DataVencimento", blank=True, null=True
    )
    valor = models.DecimalField(
        db_column="Valor", blank=True, null=True, max_digits=10, decimal_places=2
    )
    datapagamento = models.DateTimeField(
        db_column="DataPagamento", blank=True, null=True
    )
    formapagamento = models.CharField(
        db_column="FormaPagamento", max_length=255, blank=True, null=True
    )
    observacao = models.CharField(
        db_column="Observacao", max_length=255, blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "ContasPagar"


class Contasreceber(models.Model):
    codcontareceber = models.IntegerField(
        db_column="CodContaReceber", blank=True, null=True
    )
    codvenda = models.IntegerField(db_column="CodVenda", blank=True, null=True)
    datavencimento = models.DateTimeField(
        db_column="DataVencimento", blank=True, null=True
    )
    valorparcela = models.DecimalField(
        db_column="ValorParcela", blank=True, null=True, max_digits=10, decimal_places=2
    )
    formapagamento = models.CharField(
        db_column="FormaPagamento", max_length=255, blank=True, null=True
    )
    parcela = models.CharField(
        db_column="Parcela", max_length=255, blank=True, null=True
    )
    datapagamento = models.DateTimeField(
        db_column="DataPagamento", blank=True, null=True
    )
    valorpago = models.DecimalField(
        db_column="ValorPago", blank=True, null=True, max_digits=10, decimal_places=2
    )
    observacao = models.CharField(
        db_column="Observacao", max_length=255, blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "ContasReceber"


class Fornecedores(models.Model):
    codfornecedor = models.IntegerField(
        db_column="CodFornecedor", blank=True, null=True
    )
    fornecedor = models.CharField(
        db_column="Fornecedor", max_length=255, blank=True, null=True
    )
    telefone = models.CharField(
        db_column="Telefone", max_length=255, blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "Fornecedores"


class Itemvenda(models.Model):
    coditemvenda = models.IntegerField(db_column="CodItemVenda", blank=True, null=True)
    codvenda = models.IntegerField(db_column="CodVenda", blank=True, null=True)
    codproduto = models.IntegerField(db_column="CodProduto", blank=True, null=True)
    valorvenda = models.DecimalField(
        db_column="ValorVenda", blank=True, null=True, max_digits=10, decimal_places=2
    )
    observacao = models.CharField(
        db_column="Observacao", max_length=255, blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "ItemVenda"


class Notasfiscais(models.Model):
    codnotafiscal = models.IntegerField(
        db_column="CodNotaFiscal", blank=True, null=True
    )
    numeronotafiscal = models.CharField(
        db_column="NumeroNotaFiscal", max_length=255, blank=True, null=True
    )
    codfornecedor = models.IntegerField(
        db_column="CodFornecedor", blank=True, null=True
    )
    datanotafiscal = models.DateTimeField(
        db_column="DataNotaFiscal", blank=True, null=True
    )
    valornotafiscal = models.DecimalField(
        db_column="ValorNotaFiscal",
        blank=True,
        null=True,
        max_digits=10,
        decimal_places=2,
    )
    observacao = models.CharField(
        db_column="Observacao", max_length=255, blank=True, null=True
    )
    formapagamento = models.CharField(
        db_column="FormaPagamento", max_length=255, blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "NotasFiscais"


class Pedidos(models.Model):
    codpedido = models.IntegerField(db_column="CodPedido", blank=True, null=True)
    numeropedido = models.CharField(
        db_column="NumeroPedido", max_length=255, blank=True, null=True
    )
    codfornecedor = models.IntegerField(
        db_column="CodFornecedor", blank=True, null=True
    )
    codnotafiscal = models.IntegerField(
        db_column="CodNotaFiscal", blank=True, null=True
    )
    datapedido = models.DateTimeField(db_column="DataPedido", blank=True, null=True)
    valorpedido = models.DecimalField(
        db_column="ValorPedido", blank=True, null=True, max_digits=10, decimal_places=2
    )
    observacao = models.CharField(
        db_column="Observacao", max_length=255, blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "Pedidos"


class Produtos(models.Model):
    codproduto = models.IntegerField(db_column="CodProduto", blank=True, null=True)
    codpedido = models.IntegerField(db_column="CodPedido", blank=True, null=True)
    codprodutofornecedor = models.CharField(
        db_column="CodProdutoFornecedor", max_length=255, blank=True, null=True
    )
    referencia = models.CharField(
        db_column="Referencia", max_length=255, blank=True, null=True
    )
    descricao = models.CharField(
        db_column="Descricao", max_length=255, blank=True, null=True
    )
    valorcusto = models.DecimalField(
        db_column="ValorCusto", blank=True, null=True, max_digits=10, decimal_places=2
    )

    class Meta:
        managed = False
        db_table = "Produtos"


class Vendas(models.Model):
    codvenda = models.IntegerField(db_column="CodVenda", blank=True, null=True)
    codcliente = models.IntegerField(db_column="CodCliente", blank=True, null=True)
    datavenda = models.DateTimeField(db_column="DataVenda", blank=True, null=True)
    valorvenda = models.DecimalField(
        db_column="ValorVenda", blank=True, null=True, max_digits=10, decimal_places=2
    )
    observacao = models.CharField(
        db_column="Observacao", max_length=255, blank=True, null=True
    )
    condicaopagamento = models.CharField(
        db_column="CondicaoPagamento", max_length=255, blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "Vendas"
