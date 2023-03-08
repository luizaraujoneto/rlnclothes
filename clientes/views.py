from django.shortcuts import render

# Create your views here.

from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Clientes


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
