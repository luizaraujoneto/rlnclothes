from django.db import models

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
        blank=True,
        null=True,
    )

    tipopagamento = models.CharField(
        db_column="tipopagamento", max_length=1, blank=True, null=True
    )

    datapagamento = models.DateField(db_column="datapagamento", blank=True, null=True)
    valorpagamento = models.DecimalField(
        db_column="valorpagamento",
        blank=True,
        null=True,
        max_digits=6,
        decimal_places=2,
    )
    formapagamento = models.CharField(
        db_column="formapagamento", max_length=255, blank=True, null=True
    )
    observacao = models.CharField(
        db_column="observacao", max_length=255, blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "pagamentos"
