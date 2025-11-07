import django_filters
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit, HTML, Field, Fieldset, Div

from .models import Clientes, HistoricoCliente

from datetime import date
from dateutil.relativedelta import relativedelta

class ClientesFilter(django_filters.FilterSet):
    
    nomecliente = django_filters.CharFilter(
        lookup_expr='icontains',
        label="Nome do Cliente: ",
        widget=django_filters.widgets.forms.TextInput(
            attrs={'placeholder': 'Buscar por nome...'}
        )        
    ) 

    possuiparcelasematraso = django_filters.BooleanFilter(
        label="Parcelas em atraso",
        method="filter_possuiparcelasematraso",
        widget=forms.CheckboxInput(),
    )

    possuisaldoemaberto = django_filters.BooleanFilter(
        label="Saldo em aberto",
        method="filter_possuisaldo",
        widget=forms.CheckboxInput(),
    )

    possuimovimentacao = django_filters.BooleanFilter(
        label="Movimentação nos últimos 6 meses",
        method="filter_commovimentacao",
        widget=forms.CheckboxInput(),
    )

    # Com movimentação a menos de 6 meses

    class Meta:
        model = Clientes
        fields = ["nomecliente", "possuiparcelasematraso", "possuisaldoemaberto", "possuimovimentacao" ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = "get"
        self.helper.form_class = "w-100"  # ocupa toda a linha
        self.helper.label_class = "font-weight-bold"

        self.helper.layout = Layout(
            Fieldset( 
                "Filtro",
                Row(
                    Column("nomecliente", css_class="col-md-8"),
                    Column(
                        Div(
                            HTML( " <label>Exibir Clientes com: </label>"),
                            Field("possuiparcelasematraso"),
                            Field("possuisaldoemaberto" ),
                            Field("possuimovimentacao"),
                        ),
                        css_class="col-md-4 d-flex align-items-center"
                    ),
                ),
                Row(                
                    Column(
                        Div( 
                            Submit("submit", "Filtrar", css_class="btn btn-primary mr-2"),
                            HTML('<a href="." class="btn btn-secondary" role="button">Limpar</a>'),
                        ),
                        css_class="col-md-4 d-flex align-items-center"
                    ),
                    css_class="align-items-end"
                ),
                css_class="border rounded p-3"
            )
        )

    def filter_possuiparcelasematraso(self, queryset, name, value):
        if value:
            codclientes = [c.codcliente for c in queryset if c.possuiParcelaEmAtraso() == value]
            return queryset.filter(codcliente__in=codclientes)
        return queryset
    
    def filter_possuisaldo(self, queryset, name, value):
        if value:
            codclientes = [c.codcliente for c in queryset if c.saldocliente() != 0 ]
            return queryset.filter(codcliente__in=codclientes)
        return queryset
    
    def filter_commovimentacao(self, queryset, name, value):
        if value:
            data_limite = date.today() - relativedelta(months=6)

            codclientes = (
                HistoricoCliente
                .objects
                .filter(data__gt=data_limite)
                .values_list('cliente__codcliente', flat=True)
                .distinct()
            )

            return queryset.filter(codcliente__in=codclientes)
        
        return queryset