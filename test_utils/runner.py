from django.test.runner import DiscoverRunner
from django.db import connections, models

class ManagedModelTestRunner(DiscoverRunner):
    """
    Test runner que força managed=True para todos os models durante os testes,
    permitindo a criação de tabelas em bancos SQLite em memória.
    """
    def setup_test_environment(self, *args, **kwargs):
        from django.apps import apps
        self.unmanaged_models = []
        for app in apps.get_app_configs():
            for model in app.get_models():
                if not model._meta.managed:
                    model._meta.managed = True
                    self.unmanaged_models.append(model)
        super().setup_test_environment(*args, **kwargs)

    def teardown_test_environment(self, *args, **kwargs):
        super().teardown_test_environment(*args, **kwargs)
        # Reverte para managed=False para não afetar nada (embora o processo morra depois)
        for model in self.unmanaged_models:
            model._meta.managed = False
