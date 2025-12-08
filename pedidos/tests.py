from django.test import TestCase
from django.utils import timezone
from decimal import Decimal
from pedidos.models import Pedidos, Produtos, Devolucoes

class PedidosModelTest(TestCase):
    def setUp(self):
        self.pedido = Pedidos.objects.create(
            numeropedido="PED-001",
            tipopedido="C",
            valorpedido=Decimal("500.00"),
            datapedido=timezone.now().date(),
            observacao="Pedido Teste"
        )

    def test_pedido_creation(self):
        self.assertTrue(isinstance(self.pedido, Pedidos))
        self.assertEqual(str(self.pedido), "PED-001")
        self.assertIsNotNone(self.pedido.codpedido)
        
    def test_produto_creation(self):
        produto = Produtos.objects.create(
            pedido=self.pedido,
            descricao="Camisa Polo",
            referencia="POLO-001",
            valorcusto=Decimal("30.00")
        )
        self.assertIsNotNone(produto.codproduto)
        self.assertIn("Camisa Polo", str(produto))
        
    def test_devolucao_creation(self):
        prod = Produtos.objects.create(pedido=self.pedido, descricao="Item Ruim", valorcusto=Decimal("10"))
        devolucao = Devolucoes.objects.create(
            pedido=self.pedido,
            produto=prod
        )
        self.assertIsNotNone(devolucao.coddevolucao)
