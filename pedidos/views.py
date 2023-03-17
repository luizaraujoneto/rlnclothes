from django.shortcuts import render, redirect, get_object_or_404

# from django.http import HttpResponseRedirect
# from django.urls import reverse

import django_tables2 as tables

# Forms
from .forms import PedidosForm, ProdutosForm

# Create your views here.
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Pedidos, PedidoTable, Produtos

from vendas.models import Vendas


def pedido_list(request):
    table = PedidoTable(Pedidos.objects.all())
    table.paginate(page=request.GET.get("page", 1), per_page=25)
    return render(request, "pedidos\pedido_list.html", {"table": table})


def pedido_create(request):
    if request.method == "POST":
        form = PedidosForm(request.POST)

        if form.is_valid():
            form.save()

        return redirect("pedidos")

    else:
        form = PedidosForm(initial={})

    context = {"form": form}

    return render(request, "pedidos\pedido_create.html", context)


def pedido_delete(request, pk):
    pedido = get_object_or_404(Pedidos, codpedido=pk)

    if request.method == "POST":
        if pedido.codpedido:
            try:
                pedido.delete()
            except Exception as e:
                error_message = str(e)
                return render(
                    request,
                    "pedidos\pedido_delete.html",
                    {"pedido": pedido, "error_message": error_message},
                )

        return redirect("pedidos")

    return render(request, "pedidos\pedido_delete.html", {"pedido": pedido})


def pedido_detail(request, pk):
    pedido = get_object_or_404(Pedidos, codpedido=pk)

    context = {"pedido": pedido, "view_name": "list_produtos"}

    return render(request, "pedidos\pedido_detail.html", context)


def pedido_edit(request, pk):
    pedido = get_object_or_404(Pedidos, codpedido=pk)

    if request.method == "POST":
        form = PedidosForm(request.POST, instance=pedido)

        if form.is_valid():
            form.save()

            return redirect("pedido_detail", pedido.codpedido)

    else:
        form = PedidosForm(
            initial={
                "codpedido": pedido.codpedido,
                "numeropedido": pedido.numeropedido,
                "fornecedor": pedido.fornecedor,
                "notafiscal": pedido.notafiscal,
                "datapedido": pedido.datapedido,
                "valorpedido": "{:.2f}".format(pedido.valorpedido),
                "observacao": pedido.observacao,
            }
        )

    context = {"form": form}

    return render(request, "pedidos/pedido_edit.html", context)


def produto_edit(request, codproduto):
    produto = get_object_or_404(Produtos, codproduto=codproduto)

    pedido = get_object_or_404(Pedidos, codpedido=produto.pedido.codpedido)

    if request.method == "POST":
        form = ProdutosForm(request.POST, instance=produto)

        if form.is_valid():
            form.save()

            return redirect("pedido_detail", produto.pedido.codpedido)

    else:
        form = ProdutosForm(instance=produto)

    context = {
        "form": form,
        "pedido": pedido,
        "view_name": "edit_produto",
    }

    return render(request, "pedidos/pedido_detail.html", context)


def produto_detail(request, codproduto):
    produto = get_object_or_404(Produtos, codproduto=codproduto)

    try:
        venda = Vendas.objects.get(produto=produto)
    except:
        venda = None

    context = {
        "produto": produto,
        "venda": venda,
        "pedido": produto.pedido,
        "view_name": "detail_produto",
    }

    return render(request, "pedidos/pedido_detail.html", context)


def produto_create(request, codpedido):
    pedido = get_object_or_404(Pedidos, codpedido=codpedido)

    if request.method == "POST":
        form = ProdutosForm(request.POST)

        if form.is_valid():
            form.save()

            return redirect("pedido_detail", codpedido)

    else:
        form = ProdutosForm(initial={"pedido": pedido})

    context = {
        "form": form,
        "pedido": pedido,
        "view_name": "create_produto",
    }

    return render(request, "pedidos\pedido_detail.html", context)


def produto_delete(request, codproduto):
    produto = get_object_or_404(Produtos, codproduto=codproduto)

    if request.method == "POST":
        if produto.codproduto:
            try:
                produto.delete()
            except Exception as e:
                error_message = str(e)
                return render(
                    request,
                    "pedidos\pedido_detail.html",
                    {
                        "pedido": produto.pedido,
                        "produto": produto,
                        "view_name": "delete_produto",
                        "error_message": error_message,
                    },
                )

        return redirect("pedido_detail", produto.pedido.codpedido)

    context = {
        "produto": produto,
        "pedido": produto.pedido,
        "view_name": "delete_produto",
        "error_message": "",
    }

    return render(request, "pedidos\pedido_detail.html", context)
