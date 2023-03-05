from django.db import models

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

    datanotafiscal = models.DateTimeField(
        db_column="datanotafiscal", blank=True, null=True
    )
    valornotafiscal = models.FloatField(
        db_column="valornotafiscal", blank=True, null=True
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
