# Generated by Django 4.1.7 on 2023-03-04 22:47

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Cliente",
            fields=[
                (
                    "codcliente",
                    models.IntegerField(
                        blank=True,
                        db_column="codcliente",
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "cliente",
                    models.CharField(
                        blank=True, db_column="nomecliente", max_length=255, null=True
                    ),
                ),
                (
                    "telefone",
                    models.CharField(
                        blank=True, db_column="telefone", max_length=255, null=True
                    ),
                ),
            ],
            options={
                "db_table": "clientes",
            },
        ),
    ]
