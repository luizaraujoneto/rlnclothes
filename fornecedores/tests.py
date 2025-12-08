from django.test import TestCase
from fornecedores.models import Fornecedores

class FornecedoresModelTest(TestCase):
    def test_fornecedor_creation(self):
        fornecedor = Fornecedores.objects.create(
            fornecedor="Fornecedor Teste",
            telefone="123456789"
        )
        self.assertTrue(isinstance(fornecedor, Fornecedores))
        self.assertEqual(fornecedor.fornecedor, "Fornecedor Teste")
        # Since Fornecedores uses standard auto-increment (no custom save logic), 
        # and has IntegerField as PK, check if it got an ID.
        self.assertIsNotNone(fornecedor.codfornecedor)
