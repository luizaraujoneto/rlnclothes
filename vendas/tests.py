from django.test import TestCase
from django.utils import timezone
from decimal import Decimal
from vendas.models import Vendas
from clientes.models import Clientes
from pedidos.models import Produtos

class VendasModelTest(TestCase):
    def setUp(self):
        self.cliente = Clientes.objects.create(
            nomecliente="Cliente Vendas Test",
            telefone="111111111"
        )
        self.produto = Produtos.objects.create(
            descricao="Produto Teste",
            referencia="REF123",
            valorcusto=Decimal("10.00")
        )

    def test_venda_creation(self):
        venda = Vendas.objects.create(
            cliente=self.cliente,
            produto=self.produto,
            valorvenda=Decimal("20.00"),
            datavenda=timezone.now().date(),
            observacao="Venda teste"
        )
        self.assertTrue(isinstance(venda, Vendas))
        self.assertEqual(venda.valorvenda, Decimal("20.00"))
        self.assertIsNotNone(venda.codvenda)
        
    def test_venda_str(self):
        venda = Vendas.objects.create(
            cliente=self.cliente,
            valorvenda=Decimal("20.00")
        )
        self.assertEqual(str(venda), str(venda.codvenda))
