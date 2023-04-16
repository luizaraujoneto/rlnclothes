from django.shortcuts import render, redirect, get_object_or_404
from django.db import models
from django.db.models import F, DecimalField, ExpressionWrapper
from datetime import datetime

from decimal import Decimal, getcontext

from django.db.models.functions import ExtractMonth, ExtractYear, Concat
from django.db.models import Value, CharField, Sum

import matplotlib.pyplot as plt
from django.http import HttpResponse
from django.views import View
import os

# Create your views here.

from pedidos.models import Produtos
from vendas.models import Vendas
from clientes.models import Clientes
from pagamentos.models import Pagamentos
from notasfiscais.models import NotasFiscais, ContasPagar


def consulta_produtos_disponiveis(request):
    produtos = Produtos.objects.exclude(
        codproduto__in=Vendas.objects.all().values_list("produto")
    ).order_by("pedido__datapedido", "descricao")

    quantidade = produtos.count()

    context = {
        "produtos": produtos,
        "quantidade": quantidade,
    }

    return render(request, "consultas\consulta_produtos_disponiveis.html", context)


def consulta_detail_produto(request, codproduto):
    produto = get_object_or_404(Produtos, codproduto=codproduto)

    try:
        venda = Vendas.objects.get(produto=produto)
    except:
        venda = None

    context = {
        "produto": produto,
        "venda": venda,
        "pedido": produto.pedido,
    }

    return render(request, "consultas/consulta_detail_produto.html", context)


def consulta_saldo_por_cliente(request):
    all = Clientes.objects.all().order_by("nomecliente")

    saldos = []
    saldoclientes = Decimal("0.00")
    saldoareceber = Decimal("0.00")

    for cliente in all:
        saldo = Decimal(cliente.saldocliente())

        contasareceber = (
            Pagamentos.objects.filter(cliente=cliente)
            .filter(tipopagamento="P")
            .order_by("datapagamento")
        )

        # areceber = float(cliente.totalcontasareceber())
        areceber = Decimal(
            contasareceber.aggregate(totalcontasareceber=models.Sum("valorpagamento"))[
                "totalcontasareceber"
            ]
            or 0,
        )

        if saldo > 0:
            saldos.append(
                {
                    "cliente": cliente,
                    "saldocliente": round(saldo, 2),
                    "valorareceber": round(areceber, 2),
                    "contasareceber": contasareceber,
                }
            )
            saldoclientes = saldoclientes + saldo
            saldoareceber = saldoareceber + areceber
        elif areceber > 0:
            saldos.append(
                {
                    "cliente": cliente,
                    "saldocliente": round(saldo, 2),
                    "valorareceber": round(areceber, 2),
                    "contasareceber": contasareceber,
                }
            )
            saldoareceber = saldoareceber + areceber

    datareferencia = datetime.now()

    context = {
        "saldos": saldos,
        "saldototalclientes": saldoclientes,
        "saldocontasaReceber": saldoareceber,
        "datareferencia": datareferencia,
    }

    return render(request, "consultas/consulta_saldo_por_cliente.html", context)


def consulta_contas_receber(request):
    return consulta_pagamentos(request, tipopagamento="P")


def consulta_pagamentos_confirmados(request):
    return consulta_pagamentos(request, tipopagamento="C")


def consulta_pagamentos(request, tipopagamento):
    all = Pagamentos.objects.filter(tipopagamento=tipopagamento).order_by(
        "datapagamento"
    )

    if tipopagamento == "P":  # Pagamentos Previstos
        titulo = "Consulta de Contas a Receber"
    elif tipopagamento == "C":  # Pagamentos Confirmados
        titulo = "Consulta de Pagamentos Confirmados"
    else:
        titulo = ""

    meses = []
    mesanoatual = ""
    totalmes = Decimal("0.00")
    totalgeral = Decimal("0.00")
    pagamentosmes = []

    for p in all:
        mesanopagamento = p.datapagamento.strftime("%m/%Y")

        if mesanopagamento != mesanoatual:
            if mesanoatual != "":
                meses.append(
                    {
                        "mesano": mesanoatual,
                        "totalmes": totalmes,
                        "pagamentosmes": pagamentosmes,
                    },
                )

            mesanoatual = mesanopagamento
            pagamentosmes = []
            totalmes = Decimal("0.00")

        pagamentosmes.append(p)
        totalmes = totalmes + Decimal(p.valorpagamento)

        totalgeral = totalgeral + Decimal(p.valorpagamento)

    meses.append(
        {
            "mesano": mesanoatual,
            "totalmes": totalmes,
            "pagamentosmes": pagamentosmes,
        },
    )

    datareferencia = datetime.now()

    context = {
        "titulo": titulo,
        "meses": meses,
        "total": totalgeral,
        "datareferencia": datareferencia,
    }

    return render(request, "consultas/consulta_pagamentos.html", context)


def consulta_vendas(request):
    filtro = request.POST.get("mesanoconsulta", "__all__")

    vendas = (
        Vendas.objects.annotate(
            lucro=ExpressionWrapper(
                F("valorvenda") - F("produto__valorcusto"),
                output_field=DecimalField(),
            )
        )
        .annotate(
            percentual=ExpressionWrapper(
                (F("valorvenda") / F("produto__valorcusto") - 1) * 100,
                output_field=DecimalField(),
            )
        )
        .annotate(
            mesanovenda=Concat(
                ExtractMonth("datavenda"),
                Value("/"),
                ExtractYear("datavenda"),
                output_field=CharField(),
            )
        )
        .all()
        .order_by("datavenda")
    )

    titulo = "Vendas por Mês/Ano"

    meses = []
    mesanofiltro = []
    mesanoatual = ""
    totalcustomes = Decimal("0.00")
    totalvendasmes = Decimal("0.00")
    totalgeralcusto = Decimal("0.00")
    totalgeralvendas = Decimal("0.00")
    vendasmes = []

    m = ""
    for v in vendas.values_list("mesanovenda"):
        if v[0] != m:
            mesanofiltro.insert(0, v[0])
            m = v[0]

    for v in vendas:
        mesanovenda = v.mesanovenda  # v.datavenda.strftime("%m/%Y")

        if filtro != "__all__" and filtro != mesanovenda:
            continue

        if mesanovenda != mesanoatual:
            if mesanoatual != "":
                meses.insert(
                    0,
                    {
                        "mesano": mesanoatual,
                        "totalcustomes": totalcustomes,
                        "totalvendasmes": totalvendasmes,
                        "totallucromes": totalvendasmes - totalcustomes,
                        "vendasmes": vendasmes,
                    },
                )

            mesanoatual = mesanovenda
            vendasmes = []
            totalcustomes = Decimal("0.00")
            totalvendasmes = Decimal("0.00")

        vendasmes.append(v)
        totalcustomes = totalcustomes + Decimal(v.produto.valorcusto)
        totalvendasmes = totalvendasmes + Decimal(v.valorvenda)

        totalgeralcusto = totalgeralcusto + Decimal(v.produto.valorcusto)
        totalgeralvendas = totalgeralvendas + Decimal(v.valorvenda)

    meses.insert(
        0,
        {
            "mesano": mesanoatual,
            "totalcustomes": totalcustomes,
            "totalvendasmes": totalvendasmes,
            "totallucromes": totalvendasmes - totalcustomes,
            "vendasmes": vendasmes,
        },
    )

    datareferencia = datetime.now()

    context = {
        "titulo": titulo,
        "meses": meses,
        "totalgeralcusto": totalgeralcusto,
        "totalgeralvendas": totalgeralvendas,
        "totalgerallucro": totalgeralvendas - totalgeralcusto,
        "datareferencia": datareferencia,
        "mesanofiltro": mesanofiltro,
    }

    return render(request, "consultas/consulta_vendas.html", context)


def consulta_contaspagar(request):
    # filter(datapagamento__isnull=True)
    all = ContasPagar.objects.all().order_by("datavencimento")

    titulo = "Consulta Contas a Pagar"

    meses = []
    mesanoatual = ""
    totalparcelasmes = Decimal("0.00")
    totalpagomes = Decimal("0.00")
    totalgeralparcelas = Decimal("0.00")
    totalgeralpago = Decimal("0.00")
    contaspagarmes = []

    for c in all:
        mesanocontapagar = c.datavencimento.strftime("%m/%Y")

        if mesanocontapagar != mesanoatual:
            if mesanoatual != "":
                meses.insert(
                    0,
                    {
                        "mesano": mesanoatual,
                        "totalparcelasmes": totalparcelasmes,
                        "totalpagomes": totalpagomes,
                        "contaspagar": contaspagarmes,
                        "saldomes": totalparcelasmes - totalpagomes,
                    },
                )

            mesanoatual = mesanocontapagar
            contaspagarmes = []
            totalparcelasmes = Decimal("0.00")
            totalpagomes = Decimal("0.00")

        contaspagarmes.append(c)
        totalparcelasmes = totalparcelasmes + Decimal(c.valorparcela)

        totalgeralparcelas = totalgeralparcelas + Decimal(c.valorparcela)
        if c.datapagamento:
            totalpagomes = totalpagomes + Decimal(c.valorparcela)
            totalgeralpago = totalgeralpago + Decimal(c.valorparcela)

    meses.insert(
        0,
        {
            "mesano": mesanoatual,
            "totalparcelasmes": totalparcelasmes,
            "totalpagomes": totalpagomes,
            "contaspagar": contaspagarmes,
            "saldomes": totalparcelasmes - totalpagomes,
        },
    )

    datareferencia = datetime.now()

    context = {
        "titulo": titulo,
        "meses": meses,
        "totalparcelas": totalgeralparcelas,
        "totalpago": totalgeralpago,
        "datareferencia": datareferencia,
        "saldo": totalgeralparcelas - totalgeralpago,
    }

    return render(request, "consultas/consulta_contaspagar.html", context)


def consulta_saldonotafiscal(request):
    all = NotasFiscais.objects.all().order_by("datanotafiscal")

    notasfiscais = []

    print(all.count())

    for nf in all:
        contaspagar = ContasPagar.objects.filter(notafiscal=nf)

        totalparcelas = contaspagar.aggregate(totalparcelas=Sum("valorparcela"))[
            "totalparcelas"
        ] or Decimal("0.00")
        totalpago = contaspagar.exclude(datapagamento__isnull=True).aggregate(
            totalpago=Sum("valorparcela")
        )["totalpago"] or Decimal("0.00")

        valornotafiscal = Decimal(nf.valornotafiscal)
        totalpago = Decimal(totalpago)
        totalparcelas = Decimal(totalparcelas)
        saldo = Decimal("0.00")

        saldo = valornotafiscal - totalpago

        if (
            abs(valornotafiscal - totalparcelas) > 0.01
            or abs(valornotafiscal - totalpago) > 0.01
        ):
            notasfiscais.append(
                {
                    "codnotafiscal": nf.codnotafiscal,
                    "numeronotafiscal": nf.numeronotafiscal,
                    "datanotafiscal": nf.datanotafiscal,
                    "valornotafiscal": nf.valornotafiscal,
                    "valorparcelas": totalparcelas,
                    "valorpago": totalpago,
                    "saldo": saldo,
                }
            )

    datareferencia = datetime.now()

    context = {
        "notasfiscais": notasfiscais,
        "datareferencia": datareferencia,
    }

    return render(request, "consultas/consulta_saldonotafiscal.html", context)


class DashboardTotalAreceberVsTotalAPagar(View):
    def get(self, request):
        valorAReceber = (
            Pagamentos.objects.filter(tipopagamento="P").aggregate(
                totalcontasareceber=models.Sum("valorpagamento")
            )["totalcontasareceber"]
            or 0
        )

        valorAPagar = (
            ContasPagar.objects.filter(datapagamento__isnull=True).aggregate(
                totalapagar=Sum("valorparcela")
            )["totalapagar"]
            or 0
        )

        data = {"Valor a Receber": valorAReceber, "Valor a Pagar": valorAPagar}

        # Create a bar chart
        fig, ax = plt.subplots()
        ax.bar(data.keys(), data.values())

        # Save the chart to a PNG image
        chart_image = "dashboard.png"
        plt.savefig(chart_image)

        # Read the PNG image and return it as a response
        with open(chart_image, "rb") as f:
            response = HttpResponse(f.read(), content_type="image/png")
        response["Content-Disposition"] = "inline; filename=dashboard.png"

        # Delete the PNG image
        os.remove(chart_image)

        return response


class DashboardVendasView(View):
    def get(self, request):
        # Retrieve the 3 last sales data
        vendas = Vendas.objects.order_by("-datavenda")[:3]

        # Define the table headers
        headers = ["Data", "Cliente", "Produto", "Valor"]

        # Define the table cell text
        cell_text = []
        for venda in vendas:
            cell_text.append(
                [
                    venda.datavenda.strftime("%d-%m-%Y"),
                    venda.cliente,
                    venda.produto,
                    venda.valorvenda,
                ]
            )

        # Create the table
        fig, ax = plt.subplots(figsize=(9, 1.5))
        table = ax.table(cellText=cell_text, colLabels=headers, loc="center")

        # Set column widths
        table.auto_set_column_width([0, 1, 2, 3])

        # Format the table
        table.auto_set_font_size(False)
        table.set_fontsize(10)
        table.scale(1, 1.5)

        # Hide the axes
        ax.axis("off")

        # Save the figure
        plt.savefig("sales_table.png")

        # Return the image as a response
        with open("sales_table.png", "rb") as f:
            response = HttpResponse(f.read(), content_type="image/png")
        response["Content-Disposition"] = "inline; filename=sales_table.png"

        # Delete the temporary file
        os.remove("sales_table.png")

        return response


class DashboardPagamentosView(View):
    def get(self, request):
        # Retrieve the 3 last sales data
        pagamentos = Pagamentos.objects.filter(tipopagamento="C").order_by(
            "-datapagamento"
        )[:3]

        # Define the table headers
        headers = ["Data", "Cliente", "Forma Pagamento", "Valor"]

        # Define the table cell text
        cell_text = []
        for pagamento in pagamentos:
            cell_text.append(
                [
                    pagamento.datapagamento.strftime("%d-%m-%Y"),
                    pagamento.cliente,
                    pagamento.formapagamento,
                    pagamento.valorpagamento,
                ]
            )

        # Create the table
        fig, ax = plt.subplots(figsize=(9, 1.5))
        table = ax.table(cellText=cell_text, colLabels=headers, loc="center")

        # Set column widths
        table.auto_set_column_width([0, 1, 2, 3])

        # Format the table
        table.auto_set_font_size(False)
        table.set_fontsize(10)
        table.scale(1, 1.5)

        # Hide the axes
        ax.axis("off")

        # Save the figure
        plt.savefig("sales_table.png")

        # Return the image as a response
        with open("sales_table.png", "rb") as f:
            response = HttpResponse(f.read(), content_type="image/png")
        response["Content-Disposition"] = "inline; filename=sales_table.png"

        # Delete the temporary file
        os.remove("sales_table.png")

        return response
