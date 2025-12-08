import django_tables2 as tables
from .models import Vendas

class VendaTable(tables.Table):
    class Meta:
        model = Vendas
