from django.db import models

# Create your models here.

# anomes, mesano, tipolancamento, tipopagamento, valorpago


class FluxoCaixa(models.Model):
    anomes = models.CharField(
        db_column="anomes", blank=True, null=False, primary_key=True
    )

    mesano = models.CharField(db_column="mesano", blank=True, null=True)

    creditoconfirmado = models.DecimalField(
        db_column="creditoconfirmado",
        blank=True,
        null=True,
        max_digits=10,
        decimal_places=2,
    )
    debitoconfirmado = models.DecimalField(
        db_column="debitoconfirmado",
        blank=True,
        null=True,
        max_digits=10,
        decimal_places=2,
    )
    saldoconfirmado = models.DecimalField(
        db_column="saldoconfirmado",
        blank=True,
        null=True,
        max_digits=10,
        decimal_places=2,
    )
    creditoprevisto = models.DecimalField(
        db_column="creditoprevisto",
        blank=True,
        null=True,
        max_digits=10,
        decimal_places=2,
    )
    debitoprevisto = models.DecimalField(
        db_column="debitoprevisto",
        blank=True,
        null=True,
        max_digits=10,
        decimal_places=2,
    )
    saldoprevisto = models.DecimalField(
        db_column="saldoprevisto",
        blank=True,
        null=True,
        max_digits=10,
        decimal_places=2,
    )

    class Meta:
        managed = False
        db_table = "vw_fluxocaixa"
        ordering = ["anomes"]
