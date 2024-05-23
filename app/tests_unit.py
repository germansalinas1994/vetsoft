from django.test import TestCase
from app.models import Client
from app.models import Product
from decimal import Decimal

class ClientModelTest(TestCase):
    def test_can_create_and_get_client(self):
        Client.save_client(
            {
                "name": "Juan Sebastian Veron",
                "phone": "221555232",
                "address": "13 y 44",
                "email": "brujita75@hotmail.com",
            }
        )
        clients = Client.objects.all()
        self.assertEqual(len(clients), 1)

        self.assertEqual(clients[0].name, "Juan Sebastian Veron")
        self.assertEqual(clients[0].phone, "221555232")
        self.assertEqual(clients[0].address, "13 y 44")
        self.assertEqual(clients[0].email, "brujita75@hotmail.com")

    def test_can_update_client(self):
        Client.save_client(
            {
                "name": "Juan Sebastian Veron",
                "phone": "221555232",
                "address": "13 y 44",
                "email": "brujita75@hotmail.com",
            }
        )
        client = Client.objects.get(pk=1)

        self.assertEqual(client.phone, "221555232")

        client.update_client({"phone": "221555233"})

        client_updated = Client.objects.get(pk=1)

        self.assertEqual(client_updated.phone, "221555233")

    def test_update_client_with_error(self):
        Client.save_client(
            {
                "name": "Juan Sebastian Veron",
                "phone": "221555232",
                "address": "13 y 44",
                "email": "brujita75@hotmail.com",
            }
        )
        client = Client.objects.get(pk=1)

        self.assertEqual(client.phone, "221555232")

        client.update_client({"phone": ""})

        client_updated = Client.objects.get(pk=1)

        self.assertEqual(client_updated.phone, "221555232")


# PRODUCT
class ProductModelTest(TestCase):
    def test_can_create_and_get_product(self):
        Product.save_product(
            {
                "name": "Whiskas",
                "type": "Gato adulto",
                "price": "1454.3",
            }
        )
        products = Product.objects.all()
        self.assertEqual(len(products), 1)

        self.assertEqual(products[0].name, "Whiskas")
        self.assertEqual(products[0].type, "Gato adulto")
        self.assertEqual(products[0].price, 1454.3)

    def test_can_update_product(self):
        Product.save_product(
            {
                "name": "Whiskas",
                "type": "Gato adulto",
                "price": "1454.3",
            }
        )
        product = Product.objects.get(pk=1)

        self.assertEqual(product.price, 1454.3)

        product.update_product({"price": 1454.3})

        product_updated = Product.objects.get(pk=1)

        self.assertEqual(product_updated.price, 1454.3)

    def test_update_product_with_error(self):
        Product.save_product(
            {
                "name": "Whiskas",
                "type": "Gato adulto",
                "price": "1454.3",
            }
        )
        product = Product.objects.get(pk=1)

        self.assertEqual(product.price, 1454.3)

        product.update_product({"name": "Whiskas", "type": "Gato adulto","price": ""})

        product_updated = Product.objects.get(pk=1)

        self.assertEqual(product_updated.price, 1454.3)

    def test_product_price_no_negative(self):
        valid, errors = Product.save_product({
            "name": "DogChow",
            "type": "Perro adulto",
            "price": "-434.00"
        })
        self.assertFalse(valid)
        self.assertIn("price", errors)
        self.assertEqual(errors["price"], "Por favor ingrese un precio válido")


    def test_product_price_no_words_or_symbols(self):
        valid, errors = Product.save_product({
            "name": "DogChow",
            "type": "Perro adulto",
            "price": "-434abc/e"
        })
        self.assertFalse(valid)  
        self.assertIn("price", errors)  
        self.assertEqual(errors["price"], "Por favor ingrese un precio válido") 