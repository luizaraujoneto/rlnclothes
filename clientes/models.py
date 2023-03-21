from django.db import models
from django.db.models.functions import Cast
from django.db.models import Sum

import django_tables2 as tables


from vendas.models import Vendas
from pagamentos.models import Pagamentos

# Create your models here.


class Clientes(models.Model):
    codcliente = models.IntegerField(
        db_column="codcliente", blank=True, null=False, primary_key=True
    )
    nomecliente = models.CharField(
        db_column="nomecliente", max_length=255, blank=True, null=True
    )
    telefone = models.CharField(
        db_column="telefone", max_length=255, blank=True, null=True
    )

    class Meta:
        db_table = "clientes"

    def __str__(self):
        return self.nomecliente[:50]

    def save(self, *args, **kwargs):
        if not self.codcliente:
            max = Clientes.objects.aggregate(models.Max("codcliente"))[
                "codcliente__max"
            ]
            self.codcliente = max + 1
        super().save(*args, **kwargs)

    def totalvendas(self):
        return (
            Vendas.objects.filter(cliente=self).aggregate(
                totalvendas=models.Sum("valorvenda")
            )["totalvendas"]
            or 0
        )

    def totalpagamentos(self):
        return (
            Pagamentos.objects.filter(cliente=self)
            .filter(tipopagamento="C")
            .aggregate(totalpagamentoconfirmado=models.Sum("valorpagamento"))[
                "totalpagamentoconfirmado"
            ]
            or 0
        )

    def totalcontasareceber(self):
        return (
            Pagamentos.objects.filter(cliente=self)
            .filter(tipopagamento="P")
            .aggregate(totalcontasareceber=models.Sum("valorpagamento"))[
                "totalcontasareceber"
            ]
            or 0
        )

    def saldocliente(self):
        vendas = self.totalvendas()
        pagamentos = self.totalpagamentos()

        return float(vendas - pagamentos)

    def historico(self):
        colunas = []
        for f in HistoricoCliente()._meta.get_fields():
            colunas.append(f.name)

        dados = []
        saldo = 0.0
        for h in HistoricoCliente.objects.filter(cliente=self).values():
            linha = h
            if h["tipooperacao"] == "V":
                saldo = saldo - h["valor"]
            else:
                saldo = saldo + h["valor"]
            linha["saldo"] = saldo

            dados.append(linha)

        #        valor = 0
        #        for v in dados:
        #            if v[''] == "V":
        #                valor = valor + v[6]
        #            else:
        #                valor = valor - v[6]

        table = {"colunas": colunas, "dados": dados, "valor": saldo}

        return table

    def vendas(self):
        colunas = ["codvenda", "datavenda", "descricao", "valorvenda", "observacao"]

        dados = (
            HistoricoCliente.objects.filter(cliente=self)
            .filter(tipooperacao="V")
            .values_list("codoperacao", "data", "descricao", "valor", "observacao")
        )

        valor = 0
        for v in dados:
            valor = valor + v[3]

        table = {"colunas": colunas, "dados": dados, "valor": valor}

        return table

    def pagamentos(self, tipo):
        if tipo == "E":  # Pagamentos "E"fetivados
            colunas = ["Id", "Data Pgto.", "Forma Pgto.", "Valor Pago", "Observação"]

            dados = (
                HistoricoCliente.objects.filter(cliente=self)
                .filter(tipooperacao="P")
                .values_list("codoperacao", "data", "descricao", "valor", "observacao")
            )

            valor = 0
            for v in dados:
                valor = valor + v[3]

        elif tipo == "P":  # Pagamentos "P"revistos
            colunas = [
                "Id",
                "Descrição",
                "Data Vencimento",
                "Valor Previsto",
                "Observação",
            ]

            dados = (
                Pagamentos.objects.filter(cliente=self)
                .filter(tipopagamento="P")
                .select_related("venda")
                .values_list(
                    "codpagamento",
                    "formapagamento",
                    "datapagamento",
                    "valorpagamento",
                    "observacao",
                )
            )

            valor = 0
            for v in dados:
                valor = valor + v[3]

        table = {"colunas": colunas, "dados": dados, "valor": valor}

        return table


class ClienteTable(tables.Table):
    class Meta:
        model = Clientes


# cliente, tipooperacao, codoperacao, data, descricao, valor, observacao


class HistoricoCliente(models.Model):
    cliente = models.ForeignKey(
        Clientes,
        on_delete=models.DO_NOTHING,
        db_column="codcliente",
        to_field="codcliente",
        blank=True,
        null=True,
    )

    tipooperacao = models.CharField(
        db_column="tipooperacao", max_length=1, blank=True, null=True
    )
    codoperacao = models.IntegerField(db_column="codoperacao", blank=True, null=True)
    data = models.DateField(db_column="data", blank=True, null=True)
    descricao = models.CharField(
        db_column="descricao", max_length=255, blank=True, null=True
    )
    valor = models.DecimalField(
        db_column="valorvenda", blank=True, null=True, max_digits=6, decimal_places=2
    )
    observacao = models.CharField(
        db_column="observacao", max_length=255, blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "vw_historicocliente"
        ordering = ["data", "-tipooperacao"]
