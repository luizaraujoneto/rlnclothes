from django.conf import settings
from django.conf.urls import include
from django.urls import path
from django.contrib.auth.decorators import login_required


from . import views

urlpatterns = [
    path("", views.notasfiscais_list, name="notasfiscais"),
    path("create", views.notafiscal_create, name="notafiscal_create"),
    path(
        "<int:pk>/detail/",
        # login_required(views.notafiscal_detail),
        views.notafiscal_detail,
        name="notafiscal_detail",
    ),
    path("<int:pk>/edit/", views.notafiscal_edit, name="notafiscal_edit"),
    path("<int:pk>/delete/", views.notafiscal_delete, name="notafiscal_delete"),
    path(
        "<int:codnotafiscal>/create_contapagar",
        views.contapagar_create,
        name="contapagar_create",
    ),
    path(
        "detail_contapagar/<int:codcontapagar>",
        views.contapagar_detail,
        name="contapagar_detail",
    ),
    path(
        "edit_contapagar/<int:codcontapagar>",
        views.contapagar_edit,
        name="contapagar_edit",
    ),
    path(
        "delete_contapagar/<int:codcontapagar>",
        views.contapagar_delete,
        name="contapagar_delete",
    ),
]
