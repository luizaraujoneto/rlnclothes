from django.conf import settings
from django.conf.urls import include
from django.urls import path

from . import views

urlpatterns = [
    path("", views.consulta_produtos, name="consultas"),
    path("consulta_produtos/", views.consulta_produtos, name="consulta_produtos"),
    path(
        "consulta_detail_produto/<int:codproduto>",
        views.consulta_detail_produto,
        name="consulta_detail_produto",
    ),
]
