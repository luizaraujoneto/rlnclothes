from django.urls import path
from .views import (
    ClientesListView,
    ClientesDetailView,
    ClientesCreateView,
    ClientesUpdateView,
    ClientesDeleteView,
)

urlpatterns = [
    path("new/", ClientesCreateView.as_view(), name="cliente_new"),
    path("view/<int:pk>/", ClientesDetailView.as_view(), name="cliente_detail"),
    path("edit/<int:pk>/", ClientesUpdateView.as_view(), name="cliente_edit"),
    path("delete/<int:pk>/", ClientesDeleteView.as_view(), name="cliente_delete"),
    path("", ClientesListView.as_view(), name="clientes"),
]
