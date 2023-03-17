from django.shortcuts import render, redirect, get_object_or_404

from datetime import datetime

# Create your views here.

from pedidos.models import Produtos
from vendas.models import Vendas
from clientes.models import Clientes
from pagamentos.models import Pagamentos


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
    saldo = 0.00

    for c in all:
        s = c.saldocliente()
        if s > 0:
            clientes.append(c)
            saldo = saldo + s

    datareferencia = datetime.now()

    context = {
        "clientes": clientes,
        "saldototalclientes": saldo,
        "datareferencia": datareferencia,
    }

    return render(request, "consultas/consulta_saldo_por_cliente.html", context)


def consulta_contas_receber(request):
    all = Pagamentos.objects.filter(tipopagamento="P").order_by("datapagamento")

    meses = []
    mesanoatual = ""
    totalmes = 0.0
    totalgeral = 0.0
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
                    }
                )

            mesanoatual = mesanopagamento
            pagamentosmes = []
            totalmes = 0

        pagamentosmes.append(p)
        totalmes = totalmes + p.valorpagamento

        totalgeral = totalgeral + p.valorpagamento

    datareferencia = datetime.now()

    context = {
        "meses": meses,
        "total": totalgeral,
        "datareferencia": datareferencia,
    }

    return render(request, "consultas/consulta_contas_receber.html", context)
