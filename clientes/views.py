from django.shortcuts import render

# Create your views here.

from django.views.generic import ListView
from .models import Cliente


class ClientesView(ListView):
    model = Cliente
    template_name = "clientes.html"
