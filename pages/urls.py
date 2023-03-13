from django.urls import path
from .views import HomePageView, AboutPageView, ReportPageView

from . import views

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("about/", AboutPageView.as_view(), name="about"),
    path("relatorios/", ReportPageView.as_view(), name="relatorios"),
    path("relatorios/ficha/", views.pdf_report2, name="relatorios"),
]
