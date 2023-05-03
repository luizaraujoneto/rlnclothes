from django.shortcuts import render, redirect, get_object_or_404
from django import forms
import django_tables2 as tables

# Forms
from .forms import PedidosForm, ProdutosForm

# Create your views here.
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Pedidos, PedidoTable, Produtos

from vendas.models import Vendas
from pedidos.models import Devolucoes


def pedido_list(request):
    table = PedidoTable(Pedidos.objects.all().order_by("-datapedido"))
    table.paginate(page=request.GET.get("page", 1), per_page=25)
    return render(request, "pedidos\pedido_list.html", {"table": table})


def pedido_create(request):
    if request.method == "POST":
        form = PedidosForm(request.POST)

        pedido = form.instance

        if form.is_valid():
            pedido = form.save()

        return redirect("pedido_detail", pedido.codpedido)

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

    if pedido.tipopedido == "C":
        viewname = "list_produtos"
    else:
        viewname = "list_devolucoes"

    context = {"pedido": pedido, "view_name": viewname}

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
                "tipopedido": pedido.tipopedido,
                "notafiscal": pedido.notafiscal,
                "datapedido": pedido.datapedido,
                "valorpedido": "{:.2f}".format(pedido.valorpedido),
                "observacao": pedido.observacao,
            }
        )
        form.fields["tipopedido"].widget = forms.HiddenInput()

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

            submit_value = request.POST["submit"]
            if submit_value == "Salvar e cadastrar outro":
                return redirect("produto_create", codpedido)
            else:
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


def devolucoes_edit(request, codpedido):
    if request.method == "POST":
        codpedido = request.POST["codpedido"]
        codprodutos = request.POST["produtosdevolvidosInput"]
        submit = request.POST["submit"]

        pedido = get_object_or_404(Pedidos, codpedido=codpedido)

        devolucoes = Devolucoes.objects.filter(pedido=pedido)
        for devolucao in devolucoes:
            devolucao.delete()

        if codprodutos != "":
            codprodutos = codprodutos.split(",")
            for codproduto in codprodutos:
                produto = get_object_or_404(Produtos, codproduto=codproduto)
                d = Devolucoes(pedido=pedido, produto=produto)
                d.save()

        return redirect("pedido_detail", codpedido)

    #  request.method == 'GET'
    pedido = get_object_or_404(Pedidos, codpedido=codpedido)

    produtosdisponiveis = (
        Produtos.objects.exclude(
            codproduto__in=Vendas.objects.all().values_list("produto")
        )
        .exclude(codproduto__in=Devolucoes.objects.all().values_list("produto"))
        .order_by("descricao")
    )

    produtosdevolvidos = Produtos.objects.filter(
        codproduto__in=Devolucoes.objects.filter(pedido=pedido).values_list("produto")
    ).order_by("descricao")

    context = {
        "pedido": pedido,
        "view_name": "edit_devolucoes",
        "produtosdisponiveis": produtosdisponiveis,
        "produtosdevolvidos": produtosdevolvidos,
    }

    return render(request, "pedidos/pedido_detail.html", context)
