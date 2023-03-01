from django.db import models

# Create your models here.

# class Cliente(models.Model):
#    codigo = models.IntegerField()
#    nome = models.TextField()
#
#    def __str__(self):
#        return self.nome[:50]


class Cliente(models.Model):
    codcliente = models.IntegerField(
        db_column="CodCliente", blank=True, null=False, primary_key=True
    )
    cliente = models.CharField(
        db_column="Cliente", max_length=255, blank=True, null=True
    )
    telefone = models.CharField(
        db_column="Telefone", max_length=255, blank=True, null=True
    )

    def __str__(self):
        return self.cliente[:50]

    class Meta:
        db_table = "Clientes"
