from django.urls import path
from .views import HomePageView, AboutPageView
from . import views
from consultas.views import consulta_movimentomensal


urlpatterns = [
#    path("", HomePageView.as_view(), name="home"),
    path("", consulta_movimentomensal, name="home"),
    path("about/", AboutPageView.as_view(), name="about"),
]
