from django.shortcuts import render

import django_tables2 as tables

# Forms
from django.http import HttpResponseRedirect
from django.shortcuts import render

from .forms import PedidosForm

# Create your views here.
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Pedido, PedidoTable


class PedidosListView(ListView):
    model = Pedido
    template_name = "pedidos\pedidos.html"


class PedidosDetailView(DetailView):
    model = Pedido
    template_name = "pedidos\pedido_detail.html"


class PedidosCreateView(CreateView):
    model = Pedido
    template_name = "pedidos\pedido_new.html"
    fields = [
        "codpedido",
        "numeropedido",
        "codfornecedor",
        "codnotafiscal",
        "datapedido",
        "valorpedido",
        "observacao",
    ]
    success_url = "/pedidos/"


class PedidosUpdateView(UpdateView):
    model = Pedido
    template_name = "pedidos\pedido_edit.html"
    fields = [
        "numeropedido",
        "codfornecedor",
        "codnotafiscal",
        "datapedido",
        "valorpedido",
        "observacao",
    ]
    success_url = "/pedidos/"


class PedidosDeleteView(DeleteView):
    model = Pedido
    template_name = "pedidos\pedido_delete.html"
    success_url = reverse_lazy("pedidos")


class PedidosTableView(tables.SingleTableView):
    table_class = PedidoTable
    queryset = Pedido.objects.all()
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


table = PedidosTableView()
# table.paginate(page=request.GET.get("page", 1), per_page=25)


def get_name(request):
    # if this is a POST request we need to process the form data
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = PedidosForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect("/pedidos/")

    # if a GET (or any other method) we'll create a blank form
    else:
        form = PedidosForm()

    return render(request, "pedidos_form.html", {"form": form})
