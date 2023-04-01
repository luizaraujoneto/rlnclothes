from django.db import models
import django_tables2 as tables

from django import forms

# Create your models here.


class Pagamentos(models.Model):
    codpagamento = models.IntegerField(
        db_column="codpagamento", blank=True, null=False, primary_key=True
    )

    cliente = models.ForeignKey(
        "clientes.Clientes",
        on_delete=models.PROTECT,
        db_column="codcliente",
        to_field="codcliente",
        blank=False,
        null=False,
    )

    TIPOS_PAGAMENTO = [("C", "Confirmado"), ("P", "Previsto")]

    tipopagamento = models.CharField(
        db_column="tipopagamento",
        max_length=1,
        blank=False,
        null=False,
        choices=TIPOS_PAGAMENTO,
    )

    datapagamento = models.DateField(
        db_column="datapagamento",
        blank=False,
        null=False,
        auto_now=False,
        auto_now_add=False,
    )
    valorpagamento = models.DecimalField(
        db_column="valorpagamento",
        blank=False,
        null=False,
        max_digits=6,
        decimal_places=2,
    )
    formapagamento = models.CharField(
        db_column="formapagamento", max_length=255, blank=True, null=True
    )
    observacao = models.CharField(
        db_column="observacao", max_length=255, blank=True, null=True
    )

    def save(self, *args, **kwargs):
        if not self.codpagamento:
            max = Pagamentos.objects.aggregate(models.Max("codpagamento"))[
                "codpagamento__max"
            ]
            self.codpagamento = max + 1
        super().save(*args, **kwargs)

    class Meta:
        managed = False
        db_table = "pagamentos"


class PagamentoTable(tables.Table):
    class Meta:
        model = Pagamentos
