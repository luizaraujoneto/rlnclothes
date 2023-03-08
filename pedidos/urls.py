from django.conf import settings
from django.conf.urls import include
from django.urls import path

from . import views

urlpatterns = [
    path("", views.pedido_list, name="pedidos"),
    path("create", views.pedido_create, name="pedido_create"),
    path("<int:pk>/detail/", views.pedido_detail, name="pedido_detail"),
    path("<int:pk>/edit/", views.pedido_edit, name="pedido_edit"),
    path("<int:pk>/delete/", views.pedido_delete, name="pedido_delete"),
    path("<int:codpedido>/create_produto", views.produto_create, name="produto_create"),
    path(
        "detail_produto/<int:codproduto>", views.produto_detail, name="produto_detail"
    ),
    path("edit_produto/<int:codproduto>", views.produto_edit, name="produto_edit"),
    path(
        "delete_produto/<int:codproduto>", views.produto_delete, name="produto_delete"
    ),
]

"""
if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
        path("__debug__/", include(debug_toolbar.urls)),
    ] + urlpatterns
"""
