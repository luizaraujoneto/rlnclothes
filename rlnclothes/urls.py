"""first_website URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("clientes/", include("clientes.urls")),
    path("pedidos/", include("pedidos.urls")),
    path("notasfiscais/", include("notasfiscais.urls")),
    path("vendas/", include("vendas.urls")),
    path("pagamentos/", include("pagamentos.urls")),
    path("relatorios/", include("relatorios.urls")),
    path("consultas/", include("consultas.urls")),
    path("", include("pages.urls")),
]
