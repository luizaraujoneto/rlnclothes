from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.

from pedidos.models import Produtos
from vendas.models import Vendas


def consulta_produtos(request):
    filtro = request.GET.get("tipoconsulta", "")

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

    context = {"produtos": produtos, "quantidade": quantidade}

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
