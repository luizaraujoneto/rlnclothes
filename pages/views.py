from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView

from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

from decimal import Decimal


class HomePageView(TemplateView):
    template_name = "home.html"

    #  Total a receber e a pagar
    #  Exibir Gráfico de barras com previsão de valores a receber por mês
    #  Exibir Gráfico de barras com previsão de valores a pagar por mês
    #  Exibir Gráfico de barras com Vendas últimos 3 meses
    #  Exibir Gráfico de barras com Pagamentos recebidos últimos 3 meses
    #  Exibir Tabela com 3 últimos pagamentos
    #  Exibir Tabela com 3 últimas vendas

    def get_context_data(self, **kwargs):
        ultimospagamentos = [
            ["01/01/2023", "nome do cliente", "descrição", Decimal(100)],
            ["01/01/2023", "nome do cliente", "descrição", Decimal(100)],
            ["01/01/2023", "nome do cliente", "descrição", Decimal(100)],
        ]

        ultimasvendas = [
            ["01/01/2023", "nome do cliente", "nome do produto", Decimal(100)],
            ["01/01/2023", "nome do cliente", "nome do produto", Decimal(100)],
            ["01/01/2023", "nome do cliente", "nome do produto", Decimal(100)],
        ]

        context = super().get_context_data(**kwargs)
        context["totalareceber"] = Decimal(9999.99)
        context["totalapagar"] = Decimal(9999.99)
        context["ultimospagamentos"] = ultimospagamentos
        context["ultimasvendas"] = ultimasvendas
        return context


class AboutPageView(TemplateView):
    template_name = "about.html"


"""
def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("index")
        else:
            # exibir mensagem de erro de autenticação
            pass
    else:
        return render(request, "login.html")
"""
