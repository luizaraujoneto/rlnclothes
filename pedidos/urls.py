from django.conf import settings
from django.conf.urls import include
from django.urls import path
from .views import (
    PedidosListView,
    PedidosDetailView,
    PedidosCreateView,
    PedidosDeleteView,
    PedidosUpdateView,
    PedidosTableView,
)

urlpatterns = [
    path("new/", PedidosCreateView.as_view(), name="pedido_new"),
    path("view/<int:pk>/", PedidosDetailView.as_view(), name="pedido_detail"),
    path("edit/<int:pk>/", PedidosUpdateView.as_view(), name="pedido_edit"),
    path("delete/<int:pk>/", PedidosDeleteView.as_view(), name="pedido_delete"),
    path("table/", PedidosTableView.as_view(), name="pedido_table"),
    path("", PedidosTableView.as_view(), name="pedidos"),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
        path("__debug__/", include(debug_toolbar.urls)),
    ] + urlpatterns
