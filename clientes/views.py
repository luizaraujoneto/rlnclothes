from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.

# from django.views.generic import ListView, DetailView
# from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from .models import Clientes, ClienteTable
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


def cliente_detail(request, pk):
    cliente = get_object_or_404(Clientes, codcliente=pk)

    context = {"cliente": cliente, "view_name": "cliente_detail"}

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


"""
class ClientesListView(ListView):
    model = Clientes
    template_name = "clientes\clientes.html"


class ClientesDetailView(DetailView):
    model = Clientes
    template_name = "clientes\cliente_detail.html"


class ClientesCreateView(CreateView):
    model = Clientes
    template_name = "clientes\cliente_new.html"
    fields = ["codcliente", "cliente", "telefone"]
    success_url = "/clientes/"


class ClientesUpdateView(UpdateView):
    model = Clientes
    template_name = "clientes\cliente_edit.html"
    fields = ["cliente", "telefone"]
    success_url = "/clientes/"


class ClientesDeleteView(DeleteView):
    model = Clientes
    template_name = "clientes\cliente_delete.html"
    success_url = reverse_lazy("clientes")

"""
