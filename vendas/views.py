from django.shortcuts import render, redirect, get_object_or_404

import django_tables2 as tables


# Create your views here.
from django.urls import reverse_lazy

from .models import Vendas, VendaTable, ItemVenda
from .forms import VendasForm, ItemVendaForm


def venda_list(request):
    table = VendaTable(Vendas.objects.all())
    table.paginate(page=request.GET.get("page", 1), per_page=25)
    return render(request, "vendas/venda_list.html", {"table": table})


def venda_create(request):
    if request.method == "POST":
        form = VendasForm(request.POST)

        if form.is_valid():
            form.save()

        return redirect("vendas")

    else:
        form = VendasForm(initial={})

    context = {"form": form}

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

        return redirect("vendas")

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

    context = {"form": form}

    return render(request, "vendas/venda_edit.html", context)


def itemvenda_edit(request, coditemvenda):
    itemvenda = get_object_or_404(itemvenda, codproduto=coditemvenda)

    venda = get_object_or_404(Vendas, codpedido=itemvenda.venda.codvenda)

    if request.method == "POST":
        form = ItemVendaForm(request.POST, instance=itemvenda)

        if form.is_valid():
            form.save()

            return redirect("venda_detail", itemvenda.venda.codvenda)

    else:
        form = ItemVendaForm(instance=itemvenda)

    context = {
        "form": form,
        "venda": venda,
        "view_name": "edit_itemvenda",
    }

    return render(request, "vendas/itemvenda_detail.html", context)


def itemvenda_detail(request, coditemvenda):
    itemvenda = get_object_or_404(ItemVenda, codproduto=coditemvenda)

    context = {
        "itemvenda": itemvenda,
        "venda": itemvenda.venda,
        "view_name": "detail_itemvenda",
    }

    return render(request, "vendas/venda_detail.html", context)


def itemvenda_create(request, codvenda):
    venda = get_object_or_404(Vendas, codpedido=codvenda)

    if request.method == "POST":
        form = ItemVendaForm(request.POST)

        if form.is_valid():
            form.save()

            return redirect("venda_detail", codvenda)

    else:
        form = ItemVendaForm(initial={"venda": venda})

    context = {
        "form": form,
        "venda": venda,
        "view_name": "create_itemvenda",
    }

    return render(request, "vendas\venda_detail.html", context)


def itemvenda_delete(request, coditemvenda):
    itemvenda = get_object_or_404(ItemVenda, coditemvenda=coditemvenda)

    if request.method == "POST":
        if itemvenda.coditemvenda:
            try:
                itemvenda.delete()
            except Exception as e:
                error_message = str(e)
                return render(
                    request,
                    "vendas/venda_detail.html",
                    {
                        "vendas": itemvenda.venda,
                        "itemvenda": itemvenda,
                        "view_name": "delete_itemvenda",
                        "error_message": error_message,
                    },
                )

        return redirect("venda_detail", itemvenda.venda.codvenda)

    context = {
        "itemvenda": itemvenda,
        "venda": itemvenda.venda,
        "view_name": "delete_itemvenda",
        "error_message": "",
    }

    return render(request, "vendas/venda_detail.html", context)
