from django.db import models

# Create your models here.

# class Cliente(models.Model):
#    codigo = models.IntegerField()
#    nome = models.TextField()
#
#    def __str__(self):
#        return self.nome[:50]


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

    def __str__(self):
        return self.nomecliente[:50]

    class Meta:
        db_table = "clientes"
