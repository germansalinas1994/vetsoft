from django.test import TestCase
from app.models import Client
from app.models import Product
from decimal import Decimal
from app.models import Medicine
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

class MedicineModelTest(TestCase):
    def test_medicine_dose_cannot_be_empty(self):
        valid, errors = Medicine.save_medicine({
            "name": "Ivermectina",
            "description": "ectoparásitos y endoparásitos",
            "dose": ""
        })
        self.assertFalse(valid)
        self.assertIn("dose", errors)
        self.assertEqual(errors["dose"], "Por favor ingrese una dosis")

    def test_medicine_dose_cannot_be_less_than_1(self):
        valid, errors = Medicine.save_medicine({
            "name": "Ivermectina",
            "description": "ectoparásitos y endoparásitos",
            "dose": 0
        })
        self.assertFalse(valid)
        self.assertIn("dose", errors)
        self.assertEqual(errors["dose"], "Por favor ingrese una dosis entre 1 y 10")

    def test_medicine_dose_cannot_be_greater_than_10(self):
        valid, errors = Medicine.save_medicine({
            "name": "Ivermectina",
            "description": "ectoparásitos y endoparásitos",
            "dose": 11
        })
        self.assertFalse(valid)
        self.assertIn("dose", errors)
        self.assertEqual(errors["dose"], "Por favor ingrese una dosis entre 1 y 10")

    def test_medicine_dose_must_be_numeric(self):
        valid, errors = Medicine.save_medicine({
            "name": "Ivermectina",
            "description": "ectoparásitos y endoparásitos",
            "dose": "abc"
        })
        self.assertFalse(valid)
        self.assertIn("dose", errors)
        self.assertEqual(errors["dose"], "Por favor ingrese una dosis válida")

    def test_medicine_dose_within_valid_range(self):
        valid, errors = Medicine.save_medicine({
            "name": "Ivermectina",
            "description": "ectoparásitos y endoparásitos",
            "dose": 5
        })
        self.assertTrue(valid)
        self.assertIsNone(errors)
        medicines = Medicine.objects.all()
        self.assertEqual(len(medicines), 1)
        self.assertEqual(medicines[0].dose, 5)




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
