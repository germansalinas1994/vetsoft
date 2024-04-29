from django.urls import path
from . import views

urlpatterns = [
    path("", view=views.home, name="home"),
    path("clientes/", view=views.clients_repository, name="clients_repo"),
    path("clientes/nuevo/", view=views.clients_form, name="clients_form"),
    path("clientes/editar/<int:id>/", view=views.clients_form, name="clients_edit"),
    path("clientes/eliminar/", view=views.clients_delete, name="clients_delete"),

    path("vets/", view=views.vets_repository, name="vets_repo"),
    path("vets/nuevo/", view=views.vets_form, name="vets_form"),
    path("vets/eliminar/", view=views.vets_delete, name="vets_delete"),
    path("vets/editar/<int:id>/", view=views.vets_form, name="vets_edit"),

    path("providers/", view=views.providers_repository, name="providers_repo"),
    path("providers/nuevo/", view=views.providers_form, name="providers_form"),
    path("providers/eliminar/", view=views.providers_delete, name="providers_delete"),
    path("providers/editar/<int:id>/", view=views.providers_form, name="providers_edit"),

]
