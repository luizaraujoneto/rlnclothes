from django.conf import settings
from django.conf.urls import include
from django.urls import path

from . import views

urlpatterns = [
    path("", views.pagamento_list, name="pagamentos"),
    path("<int:pk>/detail/", views.pagamento_detail, name="pagamento_detail"),
    path("<int:pk>/edit/", views.pagamento_edit, name="pagamento_edit"),
    path("<int:pk>/delete/", views.pagamento_delete, name="pagamento_delete"),
    path("gerar/<int:codcliente>/", views.gerar_parcelas, name="gerar_parcelas"),
]
