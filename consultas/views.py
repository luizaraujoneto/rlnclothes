from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import F, FloatField, ExpressionWrapper
from datetime import datetime

from django.db.models.functions import ExtractMonth, ExtractYear, Concat
from django.db.models import Value, CharField, Sum

import decimal

# Create your views here.

from pedidos.models import Produtos
from vendas.models import Vendas
from clientes.models import Clientes
from pagamentos.models import Pagamentos
from notasfiscais.models import NotasFiscais, ContasPagar


def consulta_produtos(request):
    filtro = request.GET.get("tipoconsulta", "D")

    if filtro == "D":
        produtos = Produtos.objects.exclude(
            codproduto__in=Vendas.objects.all().values_list("produto")
        )
    elif filtro == "V":
        produtos = Produtos.objects.filter(
            codproduto__in=Vendas.objects.all().values_list("produto")
        )
    else:
        produtos = Produtos.objects.all()

    quantidade = produtos.count()

    context = {
        "produtos": produtos,
        "quantidade": quantidade,
        "tipoconsulta": filtro,
    }

    return render(request, "consultas\consulta_produtos.html", context)


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

    clientes = []
    saldoclientes = 0.00
    saldoareceber = 0.00

    for c in all:
        s = c.saldocliente()
        a = float(c.totalcontasareceber())
        if s > 0:
            clientes.append(c)
            saldoclientes = saldoclientes + s
            saldoareceber = saldoareceber + a
        elif a > 0:
            clientes.append(c)
            saldoareceber = saldoareceber + a

    datareferencia = datetime.now()

    context = {
        "clientes": clientes,
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
    totalmes = 0.0
    totalgeral = 0.0
    pagamentosmes = []

    for p in all:
        mesanopagamento = p.datapagamento.strftime("%m/%Y")

        if mesanopagamento != mesanoatual:
            if mesanoatual != "":
                meses.insert(
                    0,
                    {
                        "mesano": mesanoatual,
                        "totalmes": totalmes,
                        "pagamentosmes": pagamentosmes,
                    },
                )

            mesanoatual = mesanopagamento
            pagamentosmes = []
            totalmes = 0

        pagamentosmes.append(p)
        totalmes = totalmes + p.valorpagamento

        totalgeral = totalgeral + p.valorpagamento

    meses.insert(
        0,
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
                output_field=FloatField(),
            )
        )
        .annotate(
            percentual=ExpressionWrapper(
                (F("valorvenda") / F("produto__valorcusto") - 1) * 100,
                output_field=FloatField(),
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
    totalcustomes = 0.0
    totalvendasmes = 0.0
    totalgeralcusto = 0.0
    totalgeralvendas = 0.0
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
            totalcustomes = 0
            totalvendasmes = 0

        vendasmes.append(v)
        totalcustomes = totalcustomes + v.produto.valorcusto
        totalvendasmes = totalvendasmes + v.valorvenda

        totalgeralcusto = totalgeralcusto + v.produto.valorcusto
        totalgeralvendas = totalgeralvendas + v.valorvenda

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
    totalparcelasmes = 0.0
    totalpagomes = 0.0
    totalgeralparcelas = 0.0
    totalgeralpago = 0.0
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
            totalparcelasmes = 0.0
            totalpagomes = 0.0

        contaspagarmes.append(c)
        totalparcelasmes = totalparcelasmes + c.valorparcela

        totalgeralparcelas = totalgeralparcelas + c.valorparcela
        if c.datapagamento:
            totalpagomes = totalpagomes + c.valorparcela
            totalgeralpago = totalgeralpago + c.valorparcela

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

        totalparcelas = (
            contaspagar.aggregate(totalparcelas=Sum("valorparcela"))["totalparcelas"]
            or 0
        )
        totalpago = (
            contaspagar.exclude(datapagamento__isnull=True).aggregate(
                totalpago=Sum("valorparcela")
            )["totalpago"]
            or 0
        )

        valornotafiscal = decimal.Decimal(nf.valornotafiscal)
        totalpago = decimal.Decimal(totalpago)
        totalparcelas = decimal.Decimal(totalparcelas)
        saldo = decimal.Decimal(0.0)

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
