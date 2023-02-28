from django.urls import path
from .views import ClientesListView, ClientesDetailView

urlpatterns = [
    path("<int:pk>/", ClientesDetailView.as_view(), name="cliente_detail"),
    path("", ClientesListView.as_view(), name="clientes"),
]
