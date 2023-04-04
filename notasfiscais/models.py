from django.db import models
import django_tables2 as tables

from fornecedores.models import Fornecedores

# Create your models here.


class NotasFiscais(models.Model):
    codnotafiscal = models.IntegerField(
        db_column="codnotafiscal", blank=True, null=False, primary_key=True
    )
    numeronotafiscal = models.CharField(
        db_column="numeronotafiscal", max_length=255, blank=True, null=True
    )

    fornecedor = models.ForeignKey(
        Fornecedores,
        on_delete=models.PROTECT,
        db_column="codfornecedor",
        to_field="codfornecedor",
        blank=True,
        null=True,
    )

    datanotafiscal = models.DateField(db_column="datanotafiscal", blank=True, null=True)
    valornotafiscal = models.DecimalField(
        db_column="valornotafiscal",
        blank=True,
        null=True,
        max_digits=6,
        decimal_places=2,
    )
    observacao = models.CharField(
        db_column="observacao", max_length=255, blank=True, null=True
    )
    formapagamento = models.CharField(
        db_column="formapagamento", max_length=255, blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "notasfiscais"

    def __str__(self):
        return self.numeronotafiscal[:20]

    def save(self, *args, **kwargs):
        if not self.codnotafiscal:
            max = NotasFiscais.objects.aggregate(models.Max("codnotafiscal"))[
                "codnotafiscal__max"
            ]
            self.codnotafiscal = max + 1
        super().save(*args, **kwargs)


class NotasFiscaisTable(tables.Table):
    class Meta:
        model = NotasFiscais


# codcontapagar, codnotafiscal, parcela, datavencimento, valorparcela, datapagamento, formapagamento, observacao


class ContasPagar(models.Model):
    codcontapagar = models.IntegerField(
        db_column="codcontapagar", blank=True, null=False, primary_key=True
    )

    notafiscal = models.ForeignKey(
        NotasFiscais,
        on_delete=models.PROTECT,
        db_column="codnotafiscal",
        to_field="codnotafiscal",
        blank=True,
        null=True,
    )

    parcela = models.CharField(
        db_column="parcela",
        max_length=255,
        blank=True,
        null=True,
    )

    datavencimento = models.DateField(db_column="datavencimento", blank=True, null=True)
    valorparcela = models.DecimalField(
        db_column="valorparcela",
        blank=True,
        null=True,
        max_digits=6,
        decimal_places=2,
    )

    datapagamento = models.DateField(db_column="datapagamento", blank=True, null=True)

    formapagamento = models.CharField(
        db_column="formapagamento", max_length=255, blank=True, null=True
    )
    observacao = models.CharField(
        db_column="observacao", max_length=255, blank=True, null=True
    )

    def save(self, *args, **kwargs):
        if not self.codcontapagar:
            max = ContasPagar.objects.aggregate(models.Max("codcontapagar"))[
                "codcontapagar__max"
            ]
            self.codcontapagar = max + 1
        super().save(*args, **kwargs)

    class Meta:
        managed = False
        db_table = "contaspagar"


class ContasPagarTable(tables.Table):
    class Meta:
        model = ContasPagar
