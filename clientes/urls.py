from django.urls import path
from .views import ClientesListView

urlpatterns = [
    path("", ClientesListView.as_view(), name="clientes"),
]
