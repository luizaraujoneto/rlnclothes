from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal
from clientes.models import Clientes, HistoricoCliente
from vendas.models import Vendas
from pagamentos.models import Pagamentos

class ClientesModelTest(TestCase):
    def setUp(self):
        self.cliente = Clientes.objects.create(
            nomecliente="Cliente Teste",
            telefone="99999999",
            observacao="Observação Teste"
        )

    def test_cliente_creation(self):
        self.assertTrue(isinstance(self.cliente, Clientes))
        self.assertEqual(self.cliente.__str__(), "Cliente Teste")
        self.assertIsNotNone(self.cliente.codcliente)

    def test_totalvendas(self):
        # Create sales linked to client
        # Note: Vendas.codvenda usually auto-increments if handled by model save logic, 
        # but the model save needs existing objects to agg max unless table is empty.
        # ManagedModelTestRunner should give us an empty table.
        
        # Venda 1
        Vendas.objects.create(
            cliente=self.cliente,
            valorvenda=Decimal("100.00"),
            datavenda=timezone.now().date()
        )
        # Venda 2
        Vendas.objects.create(
            cliente=self.cliente,
            valorvenda=Decimal("50.50"),
            datavenda=timezone.now().date()
        )
        
        # Expected total: 150.50
        self.assertEqual(self.cliente.totalvendas(), Decimal("150.50"))

    def test_totalvendas_none(self):
        self.assertEqual(self.cliente.totalvendas(), Decimal("0.00"))

    def test_totalpagamentos(self):
        # Create confirmed payments (tipopagamento="C")
        Pagamentos.objects.create(
            cliente=self.cliente,
            tipopagamento="C",
            valorpagamento=Decimal("40.00"),
            datapagamento=timezone.now().date()
        )
        Pagamentos.objects.create(
            cliente=self.cliente,
            tipopagamento="C",
            valorpagamento=Decimal("60.00"),
            datapagamento=timezone.now().date()
        )
        # Create a predicted payment (should not be counted in totalpagamentos)
        Pagamentos.objects.create(
            cliente=self.cliente,
            tipopagamento="P",
            valorpagamento=Decimal("1000.00"),
            datapagamento=timezone.now().date()
        )

        self.assertEqual(self.cliente.totalpagamentos(), Decimal("100.00"))

    def test_totalcontasareceber(self):
        # Create predicted payments (tipopagamento="P")
        Pagamentos.objects.create(
            cliente=self.cliente,
            tipopagamento="P",
            valorpagamento=Decimal("200.00"),
            datapagamento=timezone.now().date()
        )
        
        self.assertEqual(self.cliente.totalcontasareceber(), Decimal("200.00"))

    def test_saldocliente(self):
        # Vendas: 100
        Vendas.objects.create(cliente=self.cliente, valorvenda=Decimal("100.00"), datavenda=timezone.now().date())
        # Pagamentos: 40
        Pagamentos.objects.create(cliente=self.cliente, tipopagamento="C", valorpagamento=Decimal("40.00"), datapagamento=timezone.now().date())

        # Saldo = 100 - 40 = 60
        self.assertEqual(self.cliente.saldocliente(), Decimal("60.00"))

    def test_possuiParcelaEmAtraso(self):
        # Future payment - not overdue
        future_date = timezone.now().date() + timedelta(days=5)
        Pagamentos.objects.create(
            cliente=self.cliente,
            tipopagamento="P",
            valorpagamento=Decimal("50.00"),
            datapagamento=future_date
        )
        self.assertFalse(self.cliente.possuiParcelaEmAtraso())

        # Past payment - overdue
        past_date = timezone.now().date() - timedelta(days=5)
        Pagamentos.objects.create(
            cliente=self.cliente,
            tipopagamento="P",
            valorpagamento=Decimal("50.00"),
            datapagamento=past_date
        )
        self.assertTrue(self.cliente.possuiParcelaEmAtraso())

    def test_historico_method(self):
        # Mocking data in the view table directly
        HistoricoCliente.objects.create(
            cliente=self.cliente,
            tipooperacao="V",
            codoperacao=1,
            data=timezone.now().date(),
            descricao="Venda 1",
            valor=Decimal("100.00"),
            observacao="Obs"
        )
        HistoricoCliente.objects.create(
            cliente=self.cliente,
            tipooperacao="P",
            codoperacao=2,
            data=timezone.now().date(),
            descricao="Pagamento 1",
            valor=Decimal("50.00"),
            observacao="Obs"
        )
        
        hist = self.cliente.historico()
        # Logic: Venda -> saldo -= valor (-100). Pagamento (other) -> saldo += valor (+50). Total -50.
        self.assertEqual(hist["valor"], Decimal("-50.00"))
        self.assertEqual(len(hist["dados"]), 2)

    def test_vendas_list_method(self):
        HistoricoCliente.objects.create(
            cliente=self.cliente,
            tipooperacao="V",
            codoperacao=10,
            data=timezone.now().date(),
            descricao="Venda Y",
            valor=Decimal("200.00"),
            observacao="Obs"
        )
        # Should rely on HistoricoCliente filter V
        vendas_data = self.cliente.vendas()
        self.assertEqual(vendas_data["valor"], Decimal("200.00"))
