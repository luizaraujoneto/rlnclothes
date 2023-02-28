from django.shortcuts import render

# Create your views here.

from django.views.generic import ListView, DetailView
from .models import Cliente


class ClientesListView(ListView):
    model = Cliente
    template_name = "clientes.html"
