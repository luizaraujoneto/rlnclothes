from django.shortcuts import render, redirect, get_object_or_404
from django.db import models
from django.db.models import F, DecimalField, ExpressionWrapper
from datetime import datetime

from decimal import Decimal, getcontext

from django.db.models.functions import ExtractMonth, ExtractYear, Concat
from django.db.models import Value, CharField, Sum

from .models import FluxoCaixa

from dateutil.rrule import rrule, MONTHLY
from dateutil.relativedelta import relativedelta
from datetime import datetime


# Create your views here.

from pedidos.models import Produtos, Devolucoes, Pedidos
from vendas.models import Vendas
from clientes.models import Clientes
from pagamentos.models import Pagamentos
from notasfiscais.models import NotasFiscais, ContasPagar


def consulta_produtos_disponiveis(request):
    produtos = (
        Produtos.objects.exclude(
            codproduto__in=Vendas.objects.all().values_list("produto")
        )
        .exclude(codproduto__in=Devolucoes.objects.all().values_list("produto"))
        .order_by("pedido__datapedido", "descricao")
    )

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
    context = consulta_pagamentos(tipopagamento="P")
    context["titulo"] = "Consulta de Contas a Receber"
    return render(request, "consultas/consulta_pagamentos.html", context)


def consulta_pagamentos_confirmados(request):
    context = consulta_pagamentos(tipopagamento="C")
    context["titulo"] = "Consulta de Pagamentos Confirmados"
    return render(request, "consultas/consulta_pagamentos.html", context)


def consulta_pagamentos(tipopagamento):
    pagamentos = Pagamentos.objects.filter(tipopagamento=tipopagamento).order_by(
        "datapagamento"
    )

    meses = []
    mesanoatual = ""
    totalmes = Decimal("0.00")
    totalgeral = Decimal("0.00")
    pagamentosmes = []

    for p in pagamentos:
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
        "meses": meses,
        "total": totalgeral,
        "datareferencia": datareferencia,
    }

    return context


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


def consulta_fluxocaixa(request):
    lancamentos = FluxoCaixa.objects.all().values()

    datareferencia = datetime.now()

    context = {
        "lancamentos": lancamentos,
        "datareferencia": datareferencia,
    }

    return render(request, "consultas/consulta_fluxocaixa.html", context)


def generate_month_list(start_date, final_date):
    month_list = []
    for dt in rrule(
        MONTHLY, dtstart=start_date, until=final_date
    ):  # + relativedelta(months=1)):
        month_list.append(dt.strftime("%m/%Y"))
    return month_list[::-1]


def consulta_movimentomensal(request):
    start_date = datetime(2021, 1, 1).date()
    final_date = datetime.now()
    meses = generate_month_list(start_date, final_date)

    mesanoselecionado = request.POST.get("mesanoconsulta", meses[0])

    mes, ano = mesanoselecionado.split("/")

    pedidos = Pedidos.objects.filter(
        datapedido__year=ano, datapedido__month=mes, tipopedido="C"
    )

    # produtosdevolvidos = Produtos.objects.filter(
    #    pedido__in=Devolucoes.objects.all()
    # )  # não exibir produtos devolvidos

    produtos = (
        Produtos.objects.filter(pedido__in=pedidos)
        #   .exclude(produtosdevolvidos)
        .order_by("pedido")
    )

    totalprodutos = produtos.aggregate(total=Sum("valorcusto"))["total"] or Decimal(0)
    quantidadeprodutos = produtos.count() or 0

    vendas = Vendas.objects.filter(
        datavenda__year=ano,
        datavenda__month=mes,
    ).order_by("datavenda")
    totalvendas = vendas.aggregate(total=Sum("valorvenda"))["total"] or Decimal(0)
    quantidadevendas = vendas.count() or 0

    pagamentos = Pagamentos.objects.filter(
        datapagamento__year=ano,
        datapagamento__month=mes,
    ).order_by("datapagamento")
    totalpagamentos = pagamentos.aggregate(total=Sum("valorpagamento"))[
        "total"
    ] or Decimal(0)
    quantidadepagamentos = pagamentos.count() or 0

    notasfiscais = NotasFiscais.objects.filter(
        datanotafiscal__year=ano,
        datanotafiscal__month=mes,
    )

    contaspagas = ContasPagar.objects.filter(
        datapagamento__year=ano,
        datapagamento__month=mes,
    ).order_by("datapagamento")
    totalcontaspagas = contaspagas.aggregate(total=Sum("valorparcela"))[
        "total"
    ] or Decimal(0)
    quantidadecontaspagas = contaspagas.count() or 0

    datareferencia = datetime.now()

    context = {
        "mesanoselecionado": mesanoselecionado,
        "meses": meses,
        "datareferencia": datareferencia,
        "produtos": produtos,
        "quantidadeprodutos": quantidadeprodutos,
        "totalprodutos": totalprodutos,
        "vendas": vendas,
        "quantidadevendas": quantidadevendas,
        "totalvendas": totalvendas,
        "pagamentos": pagamentos,
        "quantidadepagamentos": quantidadepagamentos,
        "totalpagamentos": totalpagamentos,
        "contaspagas": contaspagas,
        "quantidadecontaspagas": quantidadecontaspagas,
        "totalcontaspagas": totalcontaspagas,
    }

    return render(request, "consultas/consulta_movimentomensal.html", context)
