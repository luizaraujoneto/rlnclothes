from django.urls import path

from .views import ReportPageView

from . import views

urlpatterns = [
    path("", ReportPageView.as_view(), name="relatorios"),
    path("relatorios/ficha/", views.pdf_report, name="relatorios_ficha"),
]
