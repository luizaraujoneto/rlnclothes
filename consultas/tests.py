from django.test import TestCase
from decimal import Decimal
from consultas.models import FluxoCaixa

class FluxoCaixaModelTest(TestCase):
    def test_fluxocaixa_structure(self):
        # Since we use ManagedModelTestRunner, this view is created as a table in tests.
        fc = FluxoCaixa.objects.create(
            anomes="202501",
            mesano="01/2025",
            creditoconfirmado=Decimal("1000.00"),
            debitoconfirmado=Decimal("500.00"),
            saldoconfirmado=Decimal("500.00"),
            creditoprevisto=Decimal("1200.00"),
            debitoprevisto=Decimal("600.00"),
            saldoprevisto=Decimal("600.00")
        )
        self.assertEqual(fc.anomes, "202501")
        self.assertEqual(fc.saldoconfirmado, Decimal("500.00"))
