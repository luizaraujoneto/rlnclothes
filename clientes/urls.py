from django.urls import path
from .views import ClientesView

urlpatterns = [
    path("", ClientesView.as_view(), name="clientes"),
]
