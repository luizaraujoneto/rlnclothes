from django.shortcuts import render, redirect, get_object_or_404
from datetime import date
from django import forms
from dateutil.relativedelta import relativedelta
from decimal import Decimal
from calendar import monthrange
from django.contrib import messages

# Create your views here.

from .models import Pagamentos
from .tables import PagamentoTable
from .forms import PagamentosForm, GerarParcelasForm

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


def gerar_parcelas(request, codcliente):
    """
    View para geração automática de parcelas de pagamento.
    Implementa as regras de negócio para parcelamento do saldo do cliente.
    """
    cliente = get_object_or_404(Clientes, codcliente=codcliente)
    
    if request.method == "POST":
        form = GerarParcelasForm(request.POST)
        
        if form.is_valid():
            # Obter dados do formulário
            tipo_pgto = form.cleaned_data['tipopgto']
            descricao = form.cleaned_data['descricao']
            data_primeira_parcela = form.cleaned_data['data_primeira_parcela']
            num_parcelas = form.cleaned_data['num_parcelas']
            observacao = form.cleaned_data['observacao']
            
            # Regra 2: Se completo, apagar pagamentos não confirmados
            if tipo_pgto == 'completo':
                Pagamentos.objects.filter(
                    cliente=cliente,
                    tipopagamento='P'
                ).delete()
                
                # Calcular saldo total do cliente
                saldo_a_parcelar = cliente.saldocliente()
            else:
                # Regra 3: Calcular saldo não previsto
                saldo_total = cliente.saldocliente()
                saldo_previsto = cliente.totalcontasareceber()
                saldo_a_parcelar = saldo_total - saldo_previsto
            
            # Verificar se há saldo a parcelar
            if saldo_a_parcelar <= 0:
                messages.warning(request, 'Não há saldo a parcelar para este cliente.')
                return redirect('cliente_detail', cliente.codcliente, 'areceber_cliente')
            
            # Calcular valor de cada parcela
            valor_parcela = saldo_a_parcelar / Decimal(num_parcelas)
            valor_parcela = valor_parcela.quantize(Decimal('0.01'))
            
            # Regra 10: Calcular diferença de arredondamento
            total_parcelas = valor_parcela * num_parcelas
            diferenca = saldo_a_parcelar - total_parcelas
            
            # Criar as parcelas
            parcelas_criadas = []
            data_vencimento = data_primeira_parcela
            
            for i in range(1, num_parcelas + 1):
                # Regra 5: Formatar descrição da parcela
                descricao_parcela = f"{descricao} - PARCELA {i}/{num_parcelas}"
                
                # Regra 10: Aplicar diferença na primeira parcela
                valor_final = valor_parcela
                if i == 1:
                    valor_final += diferenca
                
                # Criar o pagamento
                pagamento = Pagamentos(
                    cliente=cliente,
                    tipopagamento='P',  # Regra 8: Tipo previsto
                    datapagamento=data_vencimento,
                    valorpagamento=valor_final,
                    formapagamento=descricao_parcela,  # Regra 5: Descrição
                    observacao=observacao  # Regra 6: Observação
                )
                pagamento.save()
                parcelas_criadas.append(pagamento)
                
                # Regra 4: Calcular próxima data de vencimento
                if i < num_parcelas:
                    # Adicionar 1 mês
                    proxima_data = data_vencimento + relativedelta(months=1)
                    
                    # Verificar se ultrapassou o último dia do mês
                    ultimo_dia_mes = monthrange(proxima_data.year, proxima_data.month)[1]
                    if proxima_data.day > ultimo_dia_mes:
                        proxima_data = proxima_data.replace(day=ultimo_dia_mes)
                    
                    data_vencimento = proxima_data
            
            # Mensagem de sucesso
            messages.success(
                request, 
                f'{len(parcelas_criadas)} parcela(s) gerada(s) com sucesso! Total: R$ {saldo_a_parcelar:.2f}'
            )
            
            return redirect('cliente_detail', cliente.codcliente, 'areceber_cliente')
    
    else:
        # Inicializar formulário com data de hoje
        form = GerarParcelasForm(initial={
            'data_primeira_parcela': date.today()
        })
    
    # Calcular informações para exibição
    saldo_total = cliente.saldocliente()
    saldo_previsto = cliente.totalcontasareceber()
    saldo_nao_previsto = saldo_total - saldo_previsto
    
    context = {
        'cliente': cliente,
        'form': form,
        'saldo_total': saldo_total,
        'saldo_previsto': saldo_previsto,
        'saldo_nao_previsto': saldo_nao_previsto,
    }
    
    return render(request, 'pagamentos/gerar_parcelas.html', context)
