from django.conf import settings
from django.conf.urls import include
from django.urls import path

from . import views

urlpatterns = [
    path("", views.venda_list, name="vendas"),
    #    path("create", views.venda_create, name="venda_create"),
    path("<int:pk>/detail/", views.venda_detail, name="venda_detail"),
    path("<int:pk>/edit/", views.venda_edit, name="venda_edit"),
    path("<int:pk>/delete/", views.venda_delete, name="venda_delete"),
]

"""
if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
        path("__debug__/", include(debug_toolbar.urls)),
    ] + urlpatterns
"""
