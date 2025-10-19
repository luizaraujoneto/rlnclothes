import django_filters
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit, HTML

from .models import Clientes

class ClientesFilter(django_filters.FilterSet):
    
    nomecliente = django_filters.CharFilter(
        lookup_expr='icontains',
        label="Nome do Cliente: ",
        widget=django_filters.widgets.forms.TextInput(
            attrs={'placeholder': 'Buscar por nome...'}
        )        
    )  
 
    # possuiparcelascomatraso = django_filters.DateFilter(field_name='date_created', lookup_expr='gte')  # Example: filter by date
    # Com movimentação a menos de 6 meses

    class Meta:
        model = Clientes
        fields = [ 'nomecliente']


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Configurando o helper do crispy
        self.helper = FormHelper()
        self.helper.form_method = 'get'   # importante: GET para filtros
        self.helper.form_class = 'form-inline'

        # Layout customizado
        self.helper.layout = Layout(
            Row(
                Column('nomecliente', css_class='form-group col-md-9 mb-0'),
                Column(
                    Submit('submit', 'Filtrar', css_class='btn btn-primary mt-3'),
                    HTML(
                        '<a title="Limpar Filtros" class="btn btn-secondary mt-3" href="." role="button">Limpar</a>'
                    ),
                    css_class='form-group col-md-3 mb-0 d-flex align-items-center'
                ),
            )
        )   