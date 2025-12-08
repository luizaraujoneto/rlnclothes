import pytest
from django.apps import apps
import django

def pytest_sessionstart(session):
    """
    Hook executado antes de qualquer teste.
    Força managed=True em todos os models unmanaged para que o 
    banco de dados de teste (SQLite) crie as tabelas.
    Replicando lógica de test_utils.runner.ManagedModelTestRunner.
    """
    # Garante que o Django está carregado
    try:
        django.setup()
    except Exception:
        pass

    unmanaged_models = []
    for app in apps.get_app_configs():
        for model in app.get_models():
            if not model._meta.managed:
                model._meta.managed = True
                unmanaged_models.append(model)
                
    # Opcional: imprimir quantos models foram alterados para debug (não aparece por padrão no pytest)
    # print(f"Alterado managed=True para {len(unmanaged_models)} modelos.")
