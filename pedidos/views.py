from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse

import django_tables2 as tables

# Forms
from .forms import PedidosForm

# Create your views here.
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Pedidos, PedidoTable, Produtos

"""
class PedidosListView(ListView):
    model = Pedidos
    template_name = "pedidos\pedidos.html"


class PedidosDeleteView(DeleteView):
    model = Pedidos
    template_name = "pedidos\pedido_delete.html"
    success_url = reverse_lazy("pedidos")


class PedidosTableView(tables.SingleTableView):
    table_class = PedidoTable
    queryset = Pedidos.objects.all()
    template_name = "pedidos\pedido_table.html"
    fields = [
        "codpedido",
        "numeropedido",
        "codfornecedor",
        "codnotafiscal",
        "datapedido",
        "valorpedido",
        "observacao",
    ]
"""


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

    context = {"pedido": pedido}

    return render(request, "pedidos\pedido_detail.html", context)


def pedido_edit(request, pk):
    pedido = get_object_or_404(Pedidos, codpedido=pk)

    if request.method == "POST":
        form = PedidosForm(request.POST, instance=pedido)

        if form.is_valid():
            form.save()

            return redirect("pedidos")

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

    context = {"form": form}  # , "view_name": request.resolver_match.view_name}

    return render(request, "pedidos/pedido_edit.html", context)
