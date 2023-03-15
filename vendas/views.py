from django.shortcuts import render, redirect, get_object_or_404
from datetime import date
from django import forms

# import django_tables2 as tables

# Create your views here.
from django.urls import reverse_lazy

from .models import Vendas, VendaTable  # , ItemVenda
from .forms import VendasForm  # , ItemVendaForm

from clientes.models import Clientes
from pedidos.models import Produtos


def venda_list(request):
    table = VendaTable(Vendas.objects.all())
    table.paginate(page=request.GET.get("page", 1), per_page=25)
    return render(request, "vendas/venda_list.html", {"table": table})


def venda_create(request, codcliente):
    cliente = get_object_or_404(Clientes, codcliente=codcliente)

    if request.method == "POST":
        form = VendasForm(request.POST)

        if form.is_valid():
            form.save()

        return redirect("cliente_detail", cliente.codcliente)

    else:
        form = VendasForm(initial={"cliente": cliente, "datavenda": date.today()})
        form.fields["produto"].queryset = Produtos.objects.exclude(
            codproduto__in=Vendas.objects.all().values_list("produto")
        )

    context = {"cliente": cliente, "form": form}

    return render(request, "vendas/venda_create.html", context)


def venda_delete(request, pk):
    venda = get_object_or_404(Vendas, codvenda=pk)

    if request.method == "POST":
        if venda.codvenda:
            try:
                venda.delete()
            except Exception as e:
                error_message = str(e)
                return render(
                    request,
                    "vendas/venda_delete.html",
                    {"venda": venda, "error_message": error_message},
                )

        return redirect("cliente_detail", venda.cliente.codcliente)

    return render(request, "vendas/venda_delete.html", {"venda": venda})


def venda_detail(request, pk):
    venda = get_object_or_404(Vendas, codvenda=pk)

    context = {"venda": venda, "view_name": "list_itemvendas"}

    return render(request, "vendas/venda_detail.html", context)


def venda_edit(request, pk):
    venda = get_object_or_404(Vendas, codvenda=pk)

    if request.method == "POST":
        form = VendasForm(request.POST, instance=venda)

        if form.is_valid():
            form.save()

            return redirect("venda_detail", venda.codvenda)

    else:
        form = VendasForm(instance=venda)
        form.fields["produto"].widget = forms.HiddenInput()

    context = {"form": form, "venda": venda}

    return render(request, "vendas/venda_edit.html", context)
