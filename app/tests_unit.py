from django.test import TestCase
from app.models import Client
from app.models import Pet
from decimal import Decimal
from datetime import datetime


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

class PetModelTest(TestCase):
    def test_can_create_and_get_pet(self):
        Pet.save_pet(
            {
                "name": "Fido",
                "breed": "Golden Retriever",
                "birthday": "01/01/2015",
                "weight": "10.50",
            }
        )
        pets = Pet.objects.all()
        self.assertEqual(len(pets), 1)

        self.assertEqual(pets[0].name, "Fido")
        self.assertEqual(pets[0].breed, "Golden Retriever")
        self.assertEqual(pets[0].birthday.strftime("%d/%m/%Y"), "01/01/2015")
        self.assertEqual(pets[0].weight, Decimal("10.50"))


    def test_can_update_pet(self):
        Pet.save_pet(
            {
                "name": "Fido",
                "breed": "Golden Retriever",
                "birthday": "01/01/2015",
                "weight": "10.50",
            }
        )
        pet = Pet.objects.get(pk=1)

        self.assertEqual(pet.weight, Decimal("10.50"))

        pet.update_pet({"weight": "12.30"})

        pet_updated = Pet.objects.get(pk=1)

        self.assertEqual(pet_updated.weight, Decimal("12.30"))

    def test_update_pet_with_error(self):
        success, errors = Pet.save_pet(
            {
                "name": "Fido",
                "breed": "Golden Retriever",
                "birthday": "01/01/2015",
                "weight": "10.50",
            }
        )
        self.assertTrue(success)
        self.assertIsNone(errors)

        pet = Pet.objects.get(pk=1)

        self.assertEqual(pet.weight, Decimal("10.50"))

        success, errors = pet.update_pet({"weight": ""})

        self.assertFalse(success)
        self.assertIn("weight", errors)

        pet_updated = Pet.objects.get(pk=1)

        self.assertEqual(pet_updated.weight, Decimal("10.50"))
