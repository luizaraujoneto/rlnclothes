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

    def test_api_buscar_ultimo_produto(self):
        produto = Produtos.objects.create(
            pedido=self.pedido,
            codprodutofornecedor="FORN-100",
            descricao="Produto Antigo",
            referencia="REF-100",
            valorcusto=Decimal("45.00")
        )
        response = self.client.get(
            "/pedidos/api/buscar-ultimo-produto/",
            {"codigo": "FORN-100", "codpedido": self.pedido.codpedido}
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["found"])
        self.assertEqual(data["referencia"], "REF-100")
        self.assertEqual(data["descricao"], "Produto Antigo")
        self.assertEqual(data["valorcusto"], "45.00")

    def test_api_buscar_ultimo_produto_nao_encontrado(self):
        response = self.client.get(
            "/pedidos/api/buscar-ultimo-produto/",
            {"codigo": "CODIGO_INEXISTENTE"}
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertFalse(data["found"])

