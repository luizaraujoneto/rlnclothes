from django.test import TestCase
from django.utils import timezone
from decimal import Decimal
from notasfiscais.models import NotasFiscais, ContasPagar
from fornecedores.models import Fornecedores

class NotasFiscaisModelTest(TestCase):
    def setUp(self):
        self.fornecedor = Fornecedores.objects.create(
            fornecedor="Fornecedor NF Teste"
        )

    def test_notafiscal_creation(self):
        nf = NotasFiscais.objects.create(
            numeronotafiscal="NF-100",
            fornecedor=self.fornecedor,
            valornotafiscal=Decimal("1000.00"),
            datanotafiscal=timezone.now().date()
        )
        self.assertTrue(isinstance(nf, NotasFiscais))
        self.assertEqual(nf.numeronotafiscal, "NF-100")
        self.assertIsNotNone(nf.codnotafiscal)

    def test_contaspagar_creation(self):
        nf = NotasFiscais.objects.create(
            numeronotafiscal="NF-200",
            valornotafiscal=Decimal("500.00")
        )
        conta = ContasPagar.objects.create(
            notafiscal=nf,
            parcela="1/1",
            valorparcela=Decimal("500.00"),
            datavencimento=timezone.now().date()
        )
        self.assertIsNotNone(conta.codcontapagar)
        self.assertEqual(conta.valorparcela, Decimal("500.00"))
