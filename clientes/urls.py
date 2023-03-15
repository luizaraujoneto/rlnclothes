from django.urls import path

from . import views

from vendas.views import venda_create

from pagamentos.views import pagamento_create

urlpatterns = [
    path("", views.cliente_list, name="clientes"),
    path("create", views.cliente_create, name="cliente_create"),
    path("<int:pk>/detail/", views.cliente_detail, name="cliente_detail"),
    path(
        "<int:pk>/detail/<slug:subview>/", views.cliente_detail, name="cliente_detail"
    ),
    path("<int:pk>/edit/", views.cliente_edit, name="cliente_edit"),
    path("<int:pk>/delete/", views.cliente_delete, name="cliente_delete"),
    path("<int:codcliente>/novavenda/", venda_create, name="cliente_novavenda"),
    path(
        "<int:codcliente>/novopagamento/",
        pagamento_create,
        name="cliente_novopagamento",
    ),
]
