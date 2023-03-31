from django.urls import path

from .views import ReportPageView

from . import views

urlpatterns = [
    path("", ReportPageView.as_view(), name="relatorios"),
    path("relatorios/clientes/", views.pdf_report2, name="relatorios_clientes"),
    path("relatorios/html_template/", views.html_report, name="relatorio_html"),
]
