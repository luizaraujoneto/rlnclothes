from django.db import models

# Create your models here.


class Cliente(models.Model):
    codigo = models.IntegerField()
    nome = models.TextField()

    def __str__(self):
        return self.nome[:50]
