from django.shortcuts import render, redirect, get_object_or_404
from datetime import date
from django import forms

# Create your views here.

from .models import Pagamentos, PagamentoTable
from .forms import PagamentosForm

from clientes.models import Clientes


def pagamento_list(request):
    table = PagamentoTable(Pagamentos.objects.all())
    table.paginate(page=request.GET.get("page", 1), per_page=25)
    return render(request, "pagamentos/pagamento_list.html", {"table": table})


def pagamento_create(request, codcliente):
    cliente = get_object_or_404(Clientes, codcliente=codcliente)

    if request.method == "POST":
        form = PagamentosForm(request.POST)

        if form.is_valid():
            form.save()

        pagamento = form.instance

        submit_value = request.POST["submit"]
        if submit_value == "Salvar e cadastrar outro":
            return redirect(
                "cliente_novopagamento",
                cliente.codcliente,
            )
        else:
            if pagamento.tipopagamento == "P":
                subview = "areceber_cliente"
            else:
                subview = "pagamentos_cliente"

            return redirect("cliente_detail", cliente.codcliente, subview)

    else:
        form = PagamentosForm(
            initial={"cliente": cliente, "datapagamento": date.today()}
        )

    context = {"cliente": cliente, "form": form}

    return render(request, "pagamentos/pagamento_create.html", context)


def pagamento_delete(request, pk):
    pagamento = get_object_or_404(Pagamentos, codpagamento=pk)

    subview = ""

    if request.method == "POST":
        if pagamento.codpagamento:
            if pagamento.tipopagamento == "P":
                subview = "areceber_cliente"
            else:
                subview = "pagamentos_cliente"

            try:
                pagamento.delete()
            except Exception as e:
                error_message = str(e)
                return render(
                    request,
                    "pagamentos/pagamento_delete.html",
                    {"pagamento": pagamento, "error_message": error_message},
                )

        return redirect("cliente_detail", pagamento.cliente.codcliente, subview)

    return render(request, "pagamentos/pagamento_delete.html", {"pagamento": pagamento})


def pagamento_detail(request, pk):
    pagamento = get_object_or_404(Pagamentos, codpagamento=pk)

    context = {"pagamento": pagamento}

    return render(request, "pagamentos/pagamento_detail.html", context)


def pagamento_edit(request, pk):
    pagamento = get_object_or_404(Pagamentos, codpagamento=pk)

    if request.method == "POST":
        form = PagamentosForm(request.POST, instance=pagamento)

        if form.is_valid():
            form.save()

            if pagamento.tipopagamento == "C":
                view_name = "pagamentos_cliente"
            else:
                view_name = "areceber_cliente"

            return redirect("cliente_detail", pagamento.cliente.codcliente, view_name)
        #    return redirect("pagamento_detail", pagamento.codpagamento)

    else:
        form = PagamentosForm(instance=pagamento)

    context = {"form": form, "pagamento": pagamento}

    return render(request, "pagamentos/pagamento_edit.html", context)
