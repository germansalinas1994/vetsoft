from django.urls import path

from . import views

urlpatterns = [
    path("", view=views.home, name="home"),
    # Clientes
    path("clientes/", view=views.clients_repository, name="clients_repo"),
    path("clientes/nuevo/", view=views.clients_form, name="clients_form"),
    path("clientes/editar/<int:id>/", view=views.clients_form, name="clients_edit"),
    path("clientes/eliminar/", view=views.clients_delete, name="clients_delete"),
    # Veterinario
    path("vets/", view=views.vets_repository, name="vets_repo"),
    path("vets/nuevo/", view=views.vets_form, name="vets_form"),
    path("vets/eliminar/", view=views.vets_delete, name="vets_delete"),
    path("vets/editar/<int:id>/", view=views.vets_form, name="vets_edit"),
    path("providers/", view=views.providers_repository, name="providers_repo"),
    path("providers/nuevo/", view=views.providers_form, name="providers_form"),
    path("providers/eliminar/", view=views.providers_delete, name="providers_delete"),
    path(
        "providers/editar/<int:id>/", view=views.providers_form, name="providers_edit",
    ),
    # Productos
    path("products/", view=views.products_repository, name="products_repo"),
    path("products/nuevo", view=views.products_form, name="products_form"),
    path("products/editar/<int:id>/", view=views.products_form, name="products_edit"),
    path("products/eliminar/", view=views.products_delete, name="products_delete"),
    path("pets/", view=views.pets_repository, name="pets_repo"),
    path("pets/nuevo/", view=views.pets_form, name="pets_form"),
    path("pets/eliminar/", view=views.pets_delete, name="pets_delete"),
    path("pets/editar/<int:id>/", view=views.pets_form, name="pets_edit"),
    path("medicines/", view=views.medicines_repository, name="medicines_repo"),
    path("medicines/nuevo/", view=views.medicines_form, name="medicines_form"),
    path("medicines/eliminar/", view=views.medicines_delete, name="medicines_delete"),
    path(
        "medicines/editar/<int:id>/", view=views.medicines_form, name="medicines_edit",
    ),
]
