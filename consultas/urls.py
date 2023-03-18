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
    path(
        "consulta_saldo_por_cliente",
        views.consulta_saldo_por_cliente,
        name="consulta_saldo_por_cliente",
    ),
    path(
        "consulta_contas_receber",
        views.consulta_contas_receber,
        name="consulta_contas_receber",
    ),
    path(
        "consulta_pagamentos_confirmados",
        views.consulta_pagamentos_confirmados,
        name="consulta_pagamentos_confirmados",
    ),
    path(
        "consulta_vendas",
        views.consulta_vendas,
        name="consulta_vendas",
    ),
]
