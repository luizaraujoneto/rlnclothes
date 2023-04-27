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
    # path(
    #     "dashboardReceberVsPagar/",
    #     views.DashboardTotalAreceberVsTotalAPagar.as_view(),
    #     name="dashboardrecebervspagar",
    # ),
    # path(
    #     "dashboardUltimasVendas/",
    #     views.DashboardVendasView.as_view(),
    #     name="dashboardultimasvendas",
    # ),
    # path(
    #     "dashboardUltimosPagamentos/",
    #     views.DashboardPagamentosView.as_view(),
    #     name="dashboardultimospagamentos",
    # ),
    # path(
    #     "dashboarvalorrecebermes/",
    #     views.DashboardValorAReceberPorMes.as_view(),
    #     name="dashboarvalorrecebermes",
    # ),
]
