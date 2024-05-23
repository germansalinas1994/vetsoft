from django.test import TestCase
from django.shortcuts import reverse
from app.models import Client
from app.models import Product


class HomePageTest(TestCase):
    def test_use_home_template(self):
        response = self.client.get(reverse("home"))
        self.assertTemplateUsed(response, "home.html")


class ClientsTest(TestCase):
    def test_repo_use_repo_template(self):
        response = self.client.get(reverse("clients_repo"))
        self.assertTemplateUsed(response, "clients/repository.html")

    def test_repo_display_all_clients(self):
        response = self.client.get(reverse("clients_repo"))
        self.assertTemplateUsed(response, "clients/repository.html")

    def test_form_use_form_template(self):
        response = self.client.get(reverse("clients_form"))
        self.assertTemplateUsed(response, "clients/form.html")

    def test_can_create_client(self):
        response = self.client.post(
            reverse("clients_form"),
            data={
                "name": "Juan Sebastian Veron",
                "phone": "221555232",
                "address": "13 y 44",
                "email": "brujita75@hotmail.com",
            },
        )
        clients = Client.objects.all()
        self.assertEqual(len(clients), 1)

        self.assertEqual(clients[0].name, "Juan Sebastian Veron")
        self.assertEqual(clients[0].phone, "221555232")
        self.assertEqual(clients[0].address, "13 y 44")
        self.assertEqual(clients[0].email, "brujita75@hotmail.com")

        self.assertRedirects(response, reverse("clients_repo"))

    def test_validation_errors_create_client(self):
        response = self.client.post(
            reverse("clients_form"),
            data={},
        )

        self.assertContains(response, "Por favor ingrese un nombre")
        self.assertContains(response, "Por favor ingrese un teléfono")
        self.assertContains(response, "Por favor ingrese un email")

    def test_should_response_with_404_status_if_client_doesnt_exists(self):
        response = self.client.get(reverse("clients_edit", kwargs={"id": 100}))
        self.assertEqual(response.status_code, 404)

    def test_validation_invalid_email(self):
        response = self.client.post(
            reverse("clients_form"),
            data={
                "name": "Juan Sebastian Veron",
                "phone": "221555232",
                "address": "13 y 44",
                "email": "brujita75",
            },
        )

        self.assertContains(response, "Por favor ingrese un email valido")

    def test_edit_user_with_valid_data(self):
        client = Client.objects.create(
            name="Juan Sebastián Veron",
            address="13 y 44",
            phone="221555232",
            email="brujita75@hotmail.com",
        )

        response = self.client.post(
            reverse("clients_form"),
            data={
                "id": client.id,
                "name": "Guido Carrillo",
            },
        )

        # redirect after post
        self.assertEqual(response.status_code, 302)

        editedClient = Client.objects.get(pk=client.id)
        self.assertEqual(editedClient.name, "Guido Carrillo")
        self.assertEqual(editedClient.phone, client.phone)
        self.assertEqual(editedClient.address, client.address)
        self.assertEqual(editedClient.email, client.email)


# Test Producto
class ProductsTest(TestCase):
    def test_repo_use_repo_template(self):
        response = self.client.get(reverse("products_repo"))
        self.assertTemplateUsed(response, "products/repository.html")

    def test_repo_display_all_products(self):
        response = self.client.get(reverse("products_repo"))
        self.assertTemplateUsed(response, "products/repository.html")

    def test_form_use_form_template(self):
        response = self.client.get(reverse("products_form"))
        self.assertTemplateUsed(response, "products/form.html")

    def test_can_create_product(self):
        response = self.client.post(
            reverse("products_form"),
            data={
                "name": "DogChow",
                "type": "Perro adulto",
                "price": "10400.50"
            },
        )
        products = Product.objects.all()
        self.assertEqual(len(products), 1)

        self.assertEqual(products[0].name, "DogChow")
        self.assertEqual(products[0].type, "Perro adulto")
        self.assertEqual(products[0].price, 10400.50)

        self.assertRedirects(response, reverse("products_repo"))

    def test_validation_errors_create_product(self):
        response = self.client.post(
            reverse("products_form"),
            data={},
        )

        self.assertContains(response, "Por favor ingrese el nombre del producto")
        self.assertContains(response, "Por favor ingrese el tipo de producto")
        self.assertContains(response, "Por favor ingrese un precio válido")

    def test_should_response_with_404_status_if_product_doesnt_exists(self):
        response = self.client.get(reverse("products_edit", kwargs={"id": 100}))
        self.assertEqual(response.status_code, 404)

    def test_validation_invalid_price(self):
        response = self.client.post(
            reverse("products_form"),
            data={
                "name": "DogChow",
                "type": "Perro adulto",
                "price": "10 mil pesos"
            },
        )

        self.assertContains(response, "Por favor ingrese un precio válido")

    def test_edit_user_with_valid_data(self):
        product = Product.objects.create(
            name="DogChow",
            type="Perro adulto",
            price="10400.50"
        )

        response = self.client.post(
            reverse("products_form"),
            data={
                "id": product.id,
                "name": "DogChow",
                "type": "Perro adulto",
                "price": "14400.50"
            },
        )

        # redirect after post
        self.assertEqual(response.status_code, 302)

        editedProduct = Product.objects.get(pk=product.id)
        self.assertEqual(editedProduct.name, "DogChow")
        self.assertEqual(editedProduct.type, product.type)
        self.assertEqual(editedProduct.price,  14400.50)
        self.assertNotEqual(editedProduct.price, product.price)
        