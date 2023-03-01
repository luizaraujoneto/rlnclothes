from django.shortcuts import render

# Create your views here.

from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Cliente


class ClientesListView(ListView):
    model = Cliente
    template_name = "clientes.html"


class ClientesDetailView(DetailView):
    model = Cliente
    template_name = "cliente_detail.html"


class ClientesCreateView(CreateView):
    model = Cliente
    template_name = "cliente_new.html"
    fields = ["codcliente", "cliente", "telefone"]
    success_url = "/clientes/"


class ClientesUpdateView(UpdateView):
    model = Cliente
    template_name = "cliente_edit.html"
    fields = ["cliente", "telefone"]
    success_url = "/clientes/"


class ClientesDeleteView(DeleteView):
    model = Cliente
    template_name = "cliente_delete.html"
    success_url = reverse_lazy("clientes")
