from django.test import TestCase
from django.utils import timezone
from decimal import Decimal
from pagamentos.models import Pagamentos
from clientes.models import Clientes

class PagamentosModelTest(TestCase):
    def setUp(self):
        self.cliente = Clientes.objects.create(
            nomecliente="Cliente Pgt Teste",
            telefone="11111111"
        )

    def test_pagamento_creation(self):
        pagamento = Pagamentos.objects.create(
            cliente=self.cliente,
            tipopagamento="C",
            valorpagamento=Decimal("100.00"),
            datapagamento=timezone.now().date(),
            observacao="Pgto Teste"
        )
        self.assertTrue(isinstance(pagamento, Pagamentos))
        self.assertEqual(pagamento.valorpagamento, Decimal("100.00"))
        self.assertIsNotNone(pagamento.codpagamento)

    def test_pagamento_previsto(self):
        pagamento = Pagamentos.objects.create(
            cliente=self.cliente,
            tipopagamento="P",
            valorpagamento=Decimal("200.00"),
            datapagamento=timezone.now().date() + timezone.timedelta(days=10)
        )
        self.assertEqual(pagamento.tipopagamento, "P")
