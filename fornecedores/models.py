from django.db import models

# Create your models here.


class Fornecedores(models.Model):
    codfornecedor = models.IntegerField(
        db_column="codfornecedor", blank=True, null=False, primary_key=True
    )
    fornecedor = models.CharField(
        db_column="nomefornecedor", max_length=255, blank=True, null=True
    )
    telefone = models.CharField(
        db_column="telefone", max_length=255, blank=True, null=True
    )

    def __str__(self) -> str:
        return self.fornecedor

    class Meta:
        managed = False
        db_table = "fornecedores"
