from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.

# from django.views.generic import ListView, DetailView
# from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from .models import Clientes, ClienteTable, HistoricoCliente
from .forms import ClientesForm


def cliente_list(request):
    table = ClienteTable(Clientes.objects.all())
    table.paginate(page=request.GET.get("page", 1), per_page=25)
    return render(request, "clientes\cliente_list.html", {"table": table})


def cliente_create(request):
    if request.method == "POST":
        form = ClientesForm(request.POST)

        if form.is_valid():
            form.save()

        return redirect("clientes")

    else:
        form = ClientesForm(initial={})

    context = {"form": form}

    return render(request, "clientes\cliente_create.html", context)


def cliente_delete(request, pk):
    cliente = get_object_or_404(Clientes, codcliente=pk)

    if request.method == "POST":
        if cliente.codcliente:
            try:
                cliente.delete()
            except Exception as e:
                error_message = str(e)
                return render(
                    request,
                    "clientes\cliente_delete.html",
                    {"cliente": cliente, "error_message": error_message},
                )

        return redirect("clientes")

    return render(request, "clientes\cliente_delete.html", {"cliente": cliente})


def cliente_detail(request, pk, subview="historico_cliente"):
    cliente = get_object_or_404(Clientes, codcliente=pk)

    if subview == "historico_cliente":
        table = HistoricoCliente.objects.filter(cliente=cliente).values_list()
    elif subview == "vendas_cliente":
        table = cliente.vendas()
    elif subview == "pagamentos_cliente":
        table = cliente.pagamentos()

    context = {
        "cliente": cliente,
        "view_name": "cliente_detail",
        "subview_name": subview,
        "table": table,
    }

    return render(request, "clientes\cliente_detail.html", context)


def cliente_edit(request, pk):
    cliente = get_object_or_404(Clientes, codcliente=pk)

    if request.method == "POST":
        form = ClientesForm(request.POST, instance=cliente)

        if form.is_valid():
            form.save()

            return redirect("cliente_detail", cliente.codcliente)

    else:
        form = ClientesForm(instance=cliente)

    context = {"form": form}

    return render(request, "clientes/cliente_edit.html", context)
