import django_tables2 as tables
from .models import Pagamentos

class PagamentoTable(tables.Table):
    class Meta:
        model = Pagamentos
