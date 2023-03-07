from django.conf import settings
from django.conf.urls import include
from django.urls import path

from . import views

urlpatterns = [
    path("create", views.pedido_create, name="pedido_create"),
    path("<int:pk>/detail/", views.pedido_detail, name="pedido_detail"),
    # path("new/", PedidosCreateView.as_view(), name="pedido_new"),
    # path("view/<int:pk>/", PedidosDetailView.as_view(), name="pedido_detail"),
    # path("edit/<int:pk>/", PedidosUpdateView.as_view(), name="pedido_edit"),
    path("<int:pk>/edit/", views.pedido_edit, name="pedido_edit"),
    path("<int:pk>/delete/", views.pedido_delete, name="pedido_delete"),
    path("", views.pedido_list, name="pedidos"),
]

"""
if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
        path("__debug__/", include(debug_toolbar.urls)),
    ] + urlpatterns
"""
