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
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)

            form.save()

            # d = form.cleaned_data

            # pedido = Pedidos()
            # pedido.codpedido = d.get("codpedido", 500)
            # pedido.numeropedido = d.get("numeropedido")
            # pedido.fornecedor = d.get("fornecedor")
            # pedido.notafiscal = d.get("notafiscal")
            # pedido.datapedido = d.get("datapedido")
            # pedido.valorpedido = d.get("valorpedido")
            # pedido.observacao = d.get("observacao")

            # pedido.save()

            return HttpResponseRedirect(reverse("/"))

        return redirect("pedidos")

    else:
        form = PedidosForm(
            initial={
                "codpedido": 500,
            }
        )

    context = {"form": form}

    return render(request, "pedidos\pedido_create.html", context)


def pedido_delete(request):
    return pedido_list(request)


def pedido_detail(request, pk):
    pedido = get_object_or_404(Pedidos, codpedido=pk)

    context = {"pedido": pedido}

    return render(request, "pedidos\pedido_detail.html", context)


def pedido_edit(request, pk):
    pedido = get_object_or_404(Pedidos, codpedido=pk)

    # If this is a POST request then process the Form data
    if request.method == "POST":
        # Create a form instance and populate it with data from the request (binding):
        form = PedidosForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            pedido.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse("/pedidos/"))

    # If this is a GET (or any other method) create the default form.
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

    context = {"form": form, "view_name": request.resolver_match.view_name}

    return render(request, "pedidos/pedido_edit.html", context)
