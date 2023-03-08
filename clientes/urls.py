from django.urls import path

"""
from .views import (
    ClientesListView,
    ClientesDetailView,
    ClientesCreateView,
    ClientesUpdateView,
    ClientesDeleteView,
)
"""
from . import views

urlpatterns = [
    path("", views.cliente_list, name="clientes"),
    path("create", views.cliente_create, name="cliente_create"),
    path("<int:pk>/detail/", views.cliente_detail, name="cliente_detail"),
    path("<int:pk>/edit/", views.cliente_edit, name="cliente_edit"),
    path("<int:pk>/delete/", views.cliente_delete, name="cliente_delete"),
]


"""
    path("new/", ClientesCreateView.as_view(), name="cliente_new"),
    path("view/<int:pk>/", ClientesDetailView.as_view(), name="cliente_detail"),
    path("edit/<int:pk>/", ClientesUpdateView.as_view(), name="cliente_edit"),
    path("delete/<int:pk>/", ClientesDeleteView.as_view(), name="cliente_delete"),
    path("", ClientesListView.as_view(), name="clientes"),
"""
