from django.urls import path
from .views import HomePageView, AboutPageView, TestPageView

urlpatterns = [
    path("teste/", TestPageView.as_view(), name="teste"),
    path("", HomePageView.as_view(), name="home"),
    path("about/", AboutPageView.as_view(), name="about"),
]
