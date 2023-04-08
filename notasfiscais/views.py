from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum

from decimal import Decimal

import django_tables2 as tables

# Forms
from .forms import NotasFiscaisForm, ContasPagarForm

# Create your views here.
from .models import NotasFiscais, NotasFiscaisTable, ContasPagar, ContasPagarTable


def notasfiscais_list(request):
    table = NotasFiscaisTable(NotasFiscais.objects.all().order_by("-datanotafiscal"))
    table.paginate(page=request.GET.get("page", 1), per_page=25)
    return render(request, "notasfiscais/notafiscal_list.html", {"table": table})


def notafiscal_create(request):
    if request.method == "POST":
        form = NotasFiscaisForm(request.POST)

        if form.is_valid():
            form.save()

        return redirect("notasfiscais")

    else:
        form = NotasFiscaisForm(initial={})

    context = {"form": form}

    return render(request, "notasfiscais/notafiscal_create.html", context)


def notafiscal_delete(request, pk):
    notafiscal = get_object_or_404(NotasFiscais, codnotafiscal=pk)

    if request.method == "POST":
        if notafiscal.codnotafiscal:
            try:
                notafiscal.delete()
            except Exception as e:
                error_message = str(e)
                return render(
                    request,
                    "notasfiscais/notafiscal_delete.html",
                    {"notafiscal": notafiscal, "error_message": error_message},
                )

        return redirect("notasfiscais")

    return render(
        request, "notasfiscais/notafiscal_delete.html", {"notafiscal": notafiscal}
    )


def notafiscal_detail(request, pk):
    notafiscal = get_object_or_404(NotasFiscais, codnotafiscal=pk)

    error_message = ""

    totalcontaspagar = ContasPagar.objects.filter(notafiscal=notafiscal).aggregate(
        totalcontaspagar=Sum("valorparcela")
    )["totalcontaspagar"] or Decimal("0.00")

    if notafiscal.valornotafiscal != totalcontaspagar:
        error_message = (
            "'Valor Nota Fiscal ("
            + "{:.2f}".format(notafiscal.valornotafiscal)
            + ")'  diferente do 'Total de Contas a Pagar Registrado ("
            + "{:.2f}".format(totalcontaspagar)
            + ")'. É necessário ajustar os lançamentos."
        )

    context = {
        "notafiscal": notafiscal,
        "view_name": "list_contaspagar",
        "error_message": error_message,
    }

    return render(request, "notasfiscais/notafiscal_detail.html", context)


def notafiscal_edit(request, pk):
    notafiscal = get_object_or_404(NotasFiscais, codnotafiscal=pk)

    if request.method == "POST":
        form = NotasFiscaisForm(request.POST, instance=notafiscal)

        if form.is_valid():
            form.save()

            return redirect("notafiscal_detail", notafiscal.codnotafiscal)

    else:
        form = NotasFiscaisForm(
            initial={
                "codnotafiscal": notafiscal.codnotafiscal,
                "numeronotafiscal": notafiscal.numeronotafiscal,
                "fornecedor": notafiscal.fornecedor,
                "datanotafiscal": notafiscal.datanotafiscal,
                "valornotafiscal": "{:.2f}".format(notafiscal.valornotafiscal),
                "observacao": notafiscal.observacao,
                "formapagamento": notafiscal.formapagamento,
            }
        )

    context = {"form": form}

    return render(request, "notasfiscais/notafiscal_edit.html", context)


def contapagar_edit(request, codcontapagar):
    contapagar = get_object_or_404(ContasPagar, codcontapagar=codcontapagar)

    notafiscal = get_object_or_404(
        NotasFiscais, codnotafiscal=contapagar.notafiscal.codnotafiscal
    )

    if request.method == "POST":
        form = ContasPagarForm(request.POST, instance=contapagar)

        if form.is_valid():
            form.save()

            return redirect("notafiscal_detail", contapagar.notafiscal.codnotafiscal)

    else:
        form = ContasPagarForm(instance=contapagar)

    context = {
        "form": form,
        "notafiscal": notafiscal,
        "view_name": "edit_contapagar",
    }

    return render(request, "notasfiscais/notafiscal_detail.html", context)


def contapagar_detail(request, codcontapagar):
    contapagar = get_object_or_404(ContasPagar, codcontapagar=codcontapagar)

    context = {
        "contapagar": contapagar,
        "notafiscal": contapagar.notafiscal,
        "view_name": "detail_contapagar",
    }

    return render(request, "notasfiscais/notafiscal_detail.html", context)


def contapagar_create(request, codnotafiscal):
    notafiscal = get_object_or_404(NotasFiscais, codnotafiscal=codnotafiscal)

    if request.method == "POST":
        form = ContasPagarForm(request.POST)

        if form.is_valid():
            form.save()

            submit_value = request.POST.get("submit")
            if submit_value == "Salvar e cadastrar outro":
                return redirect("contapagar_create", codnotafiscal)
            else:
                return redirect("notafiscal_detail", codnotafiscal)

    else:
        form = ContasPagarForm(initial={"notafiscal": notafiscal})

    context = {
        "form": form,
        "notafiscal": notafiscal,
        "view_name": "create_contapagar",
    }

    return render(request, "notasfiscais/notafiscal_detail.html", context)


def contapagar_delete(request, codcontapagar):
    contapagar = get_object_or_404(ContasPagar, codcontapagar=codcontapagar)

    if request.method == "POST":
        if contapagar.codcontapagar:
            try:
                contapagar.delete()
            except Exception as e:
                error_message = str(e)
                return render(
                    request,
                    "notafiscais/notafiscal_detail.html",
                    {
                        "notafiscal": contapagar.notafiscal,
                        "contapagar": contapagar,
                        "view_name": "delete_contapagar",
                        "error_message": error_message,
                    },
                )

        return redirect("notafiscal_detail", contapagar.notafiscal.codnotafiscal)

    context = {
        "contapagar": contapagar,
        "notafiscal": contapagar.notafiscal,
        "view_name": "delete_contapagar",
        "error_message": "",
    }

    return render(request, "notasfiscais/notafiscal_detail.html", context)
