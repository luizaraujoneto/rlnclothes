from django.urls import path
from .views import clientesView

urlpatterns = [
    path("", clientesView, name="Clientes"),
]
