from django.shortcuts import render

import django_tables2 as tables

# Create your views here.
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Pedido, PedidoTable


class PedidosListView(ListView):
    model = Pedido
    template_name = "pedidos\pedidos.html"


class PedidosTableView(tables.SingleTableView):
    table_class = PedidoTable
    queryset = Pedido.objects.all()
    template_name = "pedidos\pedido_table.html"


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
