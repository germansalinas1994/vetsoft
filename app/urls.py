from django.urls import path
from . import views

urlpatterns = [
    path("", view=views.home, name="home"),

    #Clientes
    path("clientes/", view=views.clients_repository, name="clients_repo"),
    path("clientes/nuevo/", view=views.clients_form, name="clients_form"),
    path("clientes/editar/<int:id>/", view=views.clients_form, name="clients_edit"),
    path("clientes/eliminar/", view=views.clients_delete, name="clients_delete"),

    #Veterinario
    path("vets/", view=views.vets_repository, name="vets_repo"),
    path("vets/nuevo/", view=views.vets_form, name="vets_form"),
    path("vets/eliminar/", view=views.vets_delete, name="vets_delete"),
    path("vets/editar/<int:id>/", view=views.vets_form, name="vets_edit"),

    #Productos
    path("products/", view=views.products_repository, name="products_repo"),
    path("products/nuevo", view=views.products_form, name="products_form"),
    path("products/editar/<int:id>/", view=views.products_form, name="products_edit"),
    path("products/eliminar/", view=views.products_delete, name="products_delete")
]
