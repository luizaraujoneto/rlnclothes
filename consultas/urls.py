from django.conf import settings
from django.conf.urls import include
from django.urls import path

from . import views

urlpatterns = [
    # path("", views.consulta_saldo_por_cliente, name="consultas"),
    # path("consulta_produtos/", views.consulta_produtos, name="consulta_produtos"),
    path(
        "consulta_produtos_disponiveis/",
        views.consulta_produtos_disponiveis,
        name="consulta_produtos_disponiveis",
    ),
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
    path(
        "consulta_contaspagar",
        views.consulta_contaspagar,
        name="consulta_contaspagar",
    ),
    path(
        "consulta_saldonotafiscal",
        views.consulta_saldonotafiscal,
        name="consulta_saldonotafiscal",
    ),
    path(
        "consulta_fluxocaixa",
        views.consulta_fluxocaixa,
        name="consulta_fluxocaixa",
    ),
    # Total a receber e a pagar
    # Exibir Gráfico de barras com previsão de valores a receber por mês
    # Exibir Gráfico de barras com previsão de valores a pagar por mês
    # Exibir Gráfico de barras com Vendas últimos 3 meses
    # Exibir Gráfico de barras com Pagamentos recebidos últimos 3 meses
    # Exibir Tabela com 3 últimos pagamentos
    # Exibir Tabela com 3 últimas vendas
]
