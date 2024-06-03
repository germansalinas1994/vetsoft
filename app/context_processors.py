from django.urls import reverse

links = [
    {"label": "Home", "href": reverse("home"), "icon": "bi bi-house-door"},
    {"label": "Clientes", "href": reverse("clients_repo"), "icon": "bi bi-people"},
    {"label": "Veterinarios", "href": reverse("vets_repo"), "icon": "bi bi-bag"},
    {"label": "Proveedores", "href": reverse("providers_repo"), "icon": "bi bi-person-badge"},


    {"label": "Productos", "href": reverse("products_repo"), "icon": "bi bi-box-seam"},
    {"label": "Mascotas", "href": reverse("pets_repo"), "icon": "bi bi-heart"},
    {"label": "Medicinas", "href": reverse("medicines_repo"), "icon": "bi bi-capsule"},
]


def navbar(request):
    """"Esta funcion asegura de que cada enlace en la lista de enlaces tenga una propiedad "active" """
    def add_active(link):
        copy = link.copy()

        if copy["href"] == "/":
            copy["active"] = request.path == "/"
        else:
            copy["active"] = request.path.startswith(copy.get("href", ""))

        return copy

    return {"links": map(add_active, links)}
