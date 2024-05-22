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
        # se crea una mascota
        Pet.save_pet(
            {
                "name": "Fido",
                "breed": "Golden Retriever",
                "birthday": "01/01/2015",
                "weight": "10.50",
            }
        )
        # se verifica que la mascota se haya creado correctamente
        pets = Pet.objects.all()
        # se verifica que haya una mascota
        self.assertEqual(len(pets), 1)
        # se verifica que los datos de la mascota sean correctos
        self.assertEqual(pets[0].name, "Fido")
        self.assertEqual(pets[0].breed, "Golden Retriever")
        self.assertEqual(pets[0].birthday.strftime("%d/%m/%Y"), "01/01/2015")
        self.assertEqual(pets[0].weight, Decimal("10.50"))


    def test_can_update_pet(self):
        # se crea una mascota
        Pet.save_pet(
            {
                "name": "Fido",
                "breed": "Golden Retriever",
                "birthday": "01/01/2015",
                "weight": "1.50",
            }
        )

        pet = Pet.objects.get(pk=1)
        self.assertEqual(pet.breed, "Golden Retriever")
        pet.update_pet({
                "breed": "Otra raza",
            })
        pet_updated = Pet.objects.get(pk=1)

        self.assertEqual(pet_updated.weight, Decimal("1.50"))



    def test_can_update_pet(self):
        # se crea una mascota
        Pet.save_pet(
            {
                "name": "Fido",
                "breed": "Golden Retriever",
                "birthday": "01/01/2015",
                "weight": "1.50",
            }
        )
        pet = Pet.objects.get(pk=1)
        self.assertEqual(pet.weight, Decimal("1.50"))
        pet.update_pet({
                "name": "cambio",
                "breed": "cambio",
                "birthday": "01/01/2010",
                "weight": "3333.33",
            })
        pet_updated = Pet.objects.get(pk=1)
        self.assertEqual(pet_updated.weight, Decimal("3333.33"))


    def test_update_pet_with_error(self):
        # se crea una mascota
        success, errors = Pet.save_pet(
            {
                "name": "Fido",
                "breed": "Golden Retriever",
                "birthday": "01/01/2015",
                "weight": "10.50",
            }
        )
        # se verifica que se haya creado correctamente
        self.assertTrue(success)
        # se verifica que no haya errores
        self.assertIsNone(errors)
        # se obtiene la mascota creada
        pet = Pet.objects.get(pk=1)
        # se verifica que el peso sea el correcto
        self.assertAlmostEqual(pet.weight, Decimal("10.50"))
        # se intenta actualizar la mascota con un peso vacío lo cual debería fallar
        success, errors = pet.update_pet({"weight": ""})
        # se verifica que la actualización haya fallado
        self.assertFalse(success)
        # se verifica que haya un error en el peso
        self.assertIn("weight", errors)
        # se verifica que el peso de la mascota no haya cambiado
        pet_updated = Pet.objects.get(pk=1)
        self.assertEqual(pet_updated.weight, Decimal("10.50"))

    def test_update_pet_with_error(self):
        # se crea una mascota
        success, errors = Pet.save_pet(
            {
                "name": "Fido",
                "breed": "Golden Retriever",
                "birthday": "01/01/2015",
                "weight": "10.50",
            }
        )
        # se verifica que se haya creado correctamente
        self.assertTrue(success)
        # se verifica que no haya errores
        self.assertIsNone(errors)
        # se obtiene la mascota creada
        pet = Pet.objects.get(pk=1)
        # se verifica que el peso sea el correcto
        self.assertEqual(pet.weight, Decimal("10.50"))
        # se intenta actualizar la mascota con un peso vacío lo cual debería fallar
        success, errors = pet.update_pet({"weight": "dasdsadsa"})
        # se verifica que la actualización haya fallado
        self.assertFalse(success)
        # se verifica que haya un error en el peso
        self.assertIn("weight", errors)
        # se verifica que el peso de la mascota no haya cambiado
        pet_updated = Pet.objects.get(pk=1)
        self.assertEqual(pet_updated.weight, Decimal("10.50"))

    def test_create_pet_with_error(self):
        # se crea una mascota
        Pet.save_pet(
            {
                "name": "Fido",
                "breed": "Golden Retriever",
                "birthday": "01/01/2015",
                "weight": "dsadsadsad",
            }
        )
        # se verifica que la mascota se haya creado correctamente
        pets = Pet.objects.all()
        # se verifica que no haya una mascota
        self.assertEqual(len(pets), 0)

    def test_create_pet_with_empty_weight(self):
        # se crea una mascota
        Pet.save_pet(
            {
                "name": "Fido",
                "breed": "Golden Retriever",
                "birthday": "01/01/2015",
                "weight": "",
            }
        )
        # se verifica que la mascota se haya creado correctamente
        pets = Pet.objects.all()
        # se verifica que no haya una mascota
        self.assertEqual(len(pets), 0)
