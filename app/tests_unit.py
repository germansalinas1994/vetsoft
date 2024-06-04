from decimal import Decimal

from django.test import TestCase

from app.models import (
    Breed,
    CityEnum,
    Client,
    Medicine,
    Pet,
    Product,
    Provider,
    Speciality,
    Vet,
)


class ClientModelTest(TestCase):
    """Modelo de test para la clase Client en app.models.py"""
    def test_can_create_and_get_client(self):
        """"
        Se crea un cliente y se verifica que se haya creado correctamente
        """
        Client.save_client(
            {
                "name": "Juan Sebastian Veron",
                "phone": "54221555232",
                "email": "brujita75@vetsoft.com",
                "city": CityEnum.LA_PLATA,
            },
        )
        clients = Client.objects.all()
        self.assertEqual(len(clients), 1)

        self.assertEqual(clients[0].name, "Juan Sebastian Veron")
        self.assertEqual(clients[0].phone, "54221555232")
        self.assertEqual(clients[0].email, "brujita75@vetsoft.com")
        self.assertEqual(clients[0].city, "La Plata")

    def test_can_update_client(self):
        """"
        Se crea un cliente y se verifica que se haya actualizado correctamente
        """
        Client.save_client(
            {
                "name": "Juan Sebastian Veron",
                "phone": "54221555232",
                "email": "brujita75@vetsoft.com",
                "city": CityEnum.LA_PLATA,
            },
        )
        client = Client.objects.get(pk=1)

        client.update_client(  {
                "name": "Juan Sebastian Veron",
                "phone": "54221555233",
                "email": "guido@vetsoft.com",
                "city": CityEnum.ENSENADA,
            },)

        client_updated = Client.objects.get(pk=1)

        self.assertEqual(client_updated.phone, "54221555233")
        self.assertEqual(client_updated.email, "guido@vetsoft.com")
        self.assertEqual(client_updated.city, "Ensenada")

    def test_update_client_with_error_empty_phone(self):
        """"
        Se crea un cliente y se intenta actualizar con un telefono vacio
        """
        Client.save_client(
            {
                "name": "Juan Sebastian Veron",
                "phone": "54221555232",
                "email": "brujita75@vetsoft.com",
                "city": CityEnum.ENSENADA,
            },
        )
        client = Client.objects.get(pk=1)

        client.update_client({
                "name": "Juan Sebastian Veron",
                "phone": "",
                "email": "brujita75@vetsoft.com",
                "city": CityEnum.ENSENADA,
            })

        client_updated = Client.objects.get(pk=1)

        self.assertEqual(client_updated.phone, "54221555232")

    def test_update_client_with_error_empty_city(self):
        """"
        Se crea un cliente y se intenta actualizar con una ciudad vacia
        """
        Client.save_client(
            {
                "name": "Juan Sebastian Veron",
                "phone": "54221555232",
                "city": CityEnum.ENSENADA,
                "email": "brujita75@vetsoft.com",
            },
        )
        client = Client.objects.get(pk=1)

        self.assertEqual(client.city, "Ensenada")

        client.update_client({
                "name": "Juan Sebastian Veron",
                "phone": "54221555232",
                "city": "",
                "email": "brujita75@vetsoft.com",
            })

        client_updated = Client.objects.get(pk=1)

        self.assertEqual(client_updated.city, "Ensenada")

    def test_update_client_with_error_wrong_phone(self):
        """"
        Se crea un cliente y se verifica si se puede actualizar con un telefono incorrecto
        """
        Client.save_client(
            {
                "name": "Juan Sebastian Veron",
                "phone": "54221555232",
                "email": "brujita75@vetsoft.com",
                "city": CityEnum.ENSENADA,
            },
        )
        client = Client.objects.get(pk=1)

        client.update_client({
                "name": "Juan Sebastian Veron",
                "phone": "221555232",
                "city": CityEnum.ENSENADA,
                "email": "brujita75@vetsoft.com",
            })

        client_updated = Client.objects.get(pk=1)

        self.assertEqual(client_updated.phone, "54221555232")


    def test_update_client_with_error_empty_email(self):
        """"
        Se crea un cliente y se intenta actualizar con un email vacio
        """
        Client.save_client(
            {
                "name": "Juan Sebastian Veron",
                "phone": "54221555232",
                "city": CityEnum.ENSENADA,
                "email": "brujita75@vetsoft.com",
            },
        )
        client = Client.objects.get(pk=1)

        client.update_client({
                "name": "Juan Sebastian Veron",
                "phone": "54221555232",
                "city": CityEnum.ENSENADA,
                "email": "",
            })

        client_updated = Client.objects.get(pk=1)

        self.assertEqual(client_updated.email, "brujita75@vetsoft.com")

    def test_update_client_with_error_wrong_email(self):
        """"
        Se crea un cliente y se verifica si se puede actualizar con un email incorrecto
        """
        Client.save_client(
            {
                "name": "Juan Sebastian Veron",
                "phone": "54221555232",
                "city": CityEnum.ENSENADA,
                "email": "brujita75@vetsoft.com",
            },
        )
        client = Client.objects.get(pk=1)

        client.update_client({
                "name": "Juan Sebastian Veron",
                "phone": "54221555232",
                "city": CityEnum.ENSENADA,
                "email": "brujita75@hotmail.com",
            })

        client_updated = Client.objects.get(pk=1)

        self.assertEqual(client_updated.email, "brujita75@vetsoft.com")


    def test_update_client_with_error_wrong_city(self):
        """"
        Se crea un cliente y se verifica si se puede actualizar con una ciudad incorrecta
        """
        Client.save_client(
            {
                "name": "Juan Sebastian Veron",
                "phone": "54221555232",
                "city": CityEnum.ENSENADA,
                "email": "brujita75@vetsoft.com",
            },
        )
        client = Client.objects.get(pk=1)

        self.assertEqual(client.city, "Ensenada")

        client.update_client({
                "name": "Juan Sebastian Veron",
                "phone": "54221555232",
                "city": "Con esta ciudad no funciona",
                "email": "brujita75@vetsoft.com",
            })

        client_updated = Client.objects.get(pk=1)

        self.assertEqual(client_updated.city, "Ensenada")


# PRODUCT
class ProductModelTest(TestCase):
    """Modulo de test para la clase Product en app.models.py"""
    def test_can_create_and_get_product(self):
        """"
        Se crea un producto y se verifica que se haya creado correctamente
        """
        Product.save_product(
            {
                "name": "Whiskas",
                "type": "Gato adulto",
                "price": "1454.3",
            },
        )
        products = Product.objects.all()
        self.assertEqual(len(products), 1)

        self.assertEqual(products[0].name, "Whiskas")
        self.assertEqual(products[0].type, "Gato adulto")
        self.assertEqual(products[0].price, 1454.3)

    def test_can_update_product(self):
        """"
        Se crea un producto y se verifica que se haya creado correctamente
        """
        Product.save_product(
            {
                "name": "Whiskas",
                "type": "Gato adulto",
                "price": "1454.3",
            },
        )
        product = Product.objects.get(pk=1)

        self.assertEqual(product.price, 1454.3)

        product.update_product({"price": 1454.3})

        product_updated = Product.objects.get(pk=1)

        self.assertEqual(product_updated.price, 1454.3)

    def test_update_product_with_error(self):
        """"
        Se crea un producto y se verifica que se haya creado correctamente
        """
        Product.save_product(
            {
                "name": "Whiskas",
                "type": "Gato adulto",
                "price": "1454.3",
            },
        )
        product = Product.objects.get(pk=1)

        self.assertEqual(product.price, 1454.3)

        product.update_product({"name": "Whiskas", "type": "Gato adulto","price": ""})

        product_updated = Product.objects.get(pk=1)

        self.assertEqual(product_updated.price, 1454.3)

    def test_product_price_no_negative(self):
        """"
        Se crea un producto y se verifica que se haya creado correctamente
        """
        valid, errors = Product.save_product({
            "name": "DogChow",
            "type": "Perro adulto",
            "price": "-434.00",
        })
        self.assertFalse(valid)
        self.assertIn("price", errors)
        self.assertEqual(errors["price"], "Por favor ingrese un precio válido")


    def test_product_price_no_words_or_symbols(self):
        """"
        Se crea un producto y se verifica que se haya creado correctamente
        """
        valid, errors = Product.save_product({
            "name": "DogChow",
            "type": "Perro adulto",
            "price": "-434abc/e",
        })
        self.assertFalse(valid)
        self.assertIn("price", errors)
        self.assertEqual(errors["price"], "Por favor ingrese un precio válido")

class MedicineModelTest(TestCase):
    """Modelo de test para la clase Medicine en app.models.py"""
    def test_medicine_dose_cannot_be_empty(self):
        """"
        Se crea un medicamento y se verifica que se haya creado correctamente
        """
        valid, errors = Medicine.save_medicine({
            "name": "Ivermectina",
            "description": "ectoparásitos y endoparásitos",
            "dose": "",
        })
        self.assertFalse(valid)
        self.assertIn("dose", errors)
        self.assertEqual(errors["dose"], "Por favor ingrese una dosis")

    def test_medicine_dose_cannot_be_less_than_1(self):
        """"
        Se crea un medicamento y se verifica que se haya creado correctamente
        """
        valid, errors = Medicine.save_medicine({
            "name": "Ivermectina",
            "description": "ectoparásitos y endoparásitos",
            "dose": 0,
        })
        self.assertFalse(valid)
        self.assertIn("dose", errors)
        self.assertEqual(errors["dose"], "Por favor ingrese una dosis entre 1 y 10")

    def test_medicine_dose_cannot_be_greater_than_10(self):
        """"
        Se crea un medicamento y se verifica que se haya creado correctamente
        """
        valid, errors = Medicine.save_medicine({
            "name": "Ivermectina",
            "description": "ectoparásitos y endoparásitos",
            "dose": 11,
        })
        self.assertFalse(valid)
        self.assertIn("dose", errors)
        self.assertEqual(errors["dose"], "Por favor ingrese una dosis entre 1 y 10")

    def test_medicine_dose_must_be_numeric(self):
        """"
        Se crea un medicamento y se verifica que se haya creado correctamente
        """
        valid, errors = Medicine.save_medicine({
            "name": "Ivermectina",
            "description": "ectoparásitos y endoparásitos",
            "dose": "abc",
        })
        self.assertFalse(valid)
        self.assertIn("dose", errors)
        self.assertEqual(errors["dose"], "Por favor ingrese una dosis válida")

    def test_medicine_dose_within_valid_range(self):
        """"
        Se crea un medicamento y se verifica que se haya creado correctamente
        """
        valid, errors = Medicine.save_medicine({
            "name": "Ivermectina",
            "description": "ectoparásitos y endoparásitos",
            "dose": 5,
        })
        self.assertTrue(valid)
        self.assertIsNone(errors)
        medicines = Medicine.objects.all()
        self.assertEqual(len(medicines), 1)
        self.assertEqual(medicines[0].dose, 5)




class PetModelTest(TestCase):
    """Modelo de test para la clase Pet en app.models.py"""
    def test_can_create_and_get_pet(self):
        """"
        Se crea una mascota y se verifica que se haya creado correctamente
        """
        # se crea una mascota
        Pet.save_pet(
            {
                "name": "Fido",
                "breed": Breed.GOLDEN_RETRIEVER,
                "birthday": "01/01/2015",
                "weight": "10.50",
            },
        )
        # se verifica que la mascota se haya creado correctamente
        pets = Pet.objects.all()
        # se verifica que haya una mascota
        self.assertEqual(len(pets), 1)
        # se verifica que los datos de la mascota sean correctos
        self.assertEqual(pets[0].name, "Fido")
        self.assertEqual(pets[0].breed, Breed.GOLDEN_RETRIEVER)
        self.assertEqual(pets[0].birthday.strftime("%d/%m/%Y"), "01/01/2015")
        self.assertEqual(pets[0].weight, Decimal("10.50"))

    def test_cant_create_and_get_pet(self):
        """"
        Se crea una mascota y se verifica que se haya creado correctamente
        """
        # se crea una mascota
        Pet.save_pet(
            {
                "name": "Fido",
                "breed": "Raza inexistente",
                "birthday": "01/01/2015",
                "weight": "10.50",
            },
        )
        # se verifica que la mascota se haya creado correctamente
        pets = Pet.objects.all()
        # se verifica que haya una mascota
        self.assertEqual(len(pets), 0)

    def test_can_update_pet_change_breed(self):
        """"
        Se crea una mascota y se verifica que se haya creado correctamente
        """
        # se crea una mascota
        Pet.save_pet(
            {
                "name": "Fido",
                "breed": Breed.GOLDEN_RETRIEVER,
                "birthday": "01/01/2015",
                "weight": "1.50",
            },
        )

        pet = Pet.objects.get(pk=1)
        pet.update_pet({
                "name": "Fido",
                "breed": Breed.BOXER,
                "birthday": "01/01/2015",
                "weight": "1000",
            })
        pet_updated = Pet.objects.get(pk=1)


        self.assertEqual(pet_updated.weight, Decimal("1000"))
        self.assertEqual(pet_updated.breed, Breed.BOXER)
        self.assertEqual(pet_updated.birthday.strftime("%d/%m/%Y"), "01/01/2015")
        self.assertEqual(pet_updated.name, "Fido")

    def test_can_update_pet_change_weight(self):
        """"
        Se crea una mascota y se verifica que se haya creado correctamente
        """
        # se crea una mascota
        Pet.save_pet(
            {
                "name": "Fido",
                "breed": Breed.GOLDEN_RETRIEVER,
                "birthday": "01/01/2015",
                "weight": "1.50",
            },
        )
        pet = Pet.objects.get(pk=1)
        pet.update_pet({
                "name": "cambio",
                "breed": Breed.GOLDEN_RETRIEVER,
                "birthday": "01/01/2015",
                "weight": "3333.33",
            })
        pet_updated = Pet.objects.get(pk=1)
        self.assertEqual(pet_updated.weight, Decimal("3333.33"))
        self.assertEqual(pet_updated.breed, "Golden Retriever")

    def test_update_pet_with_error_empty_breed(self):
        """"
        Se crea una mascota y se verifica que se haya creado correctamente
        """
        # se crea una mascota
        Pet.save_pet(
            {
                "name": "Fido",
                "breed": Breed.GOLDEN_RETRIEVER,
                "birthday": "01/01/2015",
                "weight": "10.50",
            },
        )
        pet = Pet.objects.get(pk=1)
        pet.update_pet({
                "name": "Fido",
                "breed": "",
                "birthday": "01/01/2015",
                "weight": "10.50",
                })
        pet_updated = Pet.objects.get(pk=1)
        self.assertEqual(pet_updated.breed, Breed.GOLDEN_RETRIEVER)

    def test_update_pet_with_error_bad_breed(self):
        """"
        Se crea una mascota y se verifica que se haya creado correctamente
        """
        # se crea una mascota
        Pet.save_pet(
            {
                "name": "Fido",
                "breed": Breed.GOLDEN_RETRIEVER,
                "birthday": "01/01/2015",
                "weight": "10.50",
            },
        )
        pet = Pet.objects.get(pk=1)
        pet.update_pet({
                "name": "Fido",
                "breed": "Con esta raza no deberia updatear",
                "birthday": "01/01/2015",
                "weight": "10.50",
                })
        pet_updated = Pet.objects.get(pk=1)
        self.assertEqual(pet_updated.breed, Breed.GOLDEN_RETRIEVER)

    def test_update_pet_with_error_bad_weight(self):
        """"
        Se crea una mascota y se verifica que se haya creado correctamente
        """
        # se crea una mascota
        Pet.save_pet(
            {
                "name": "Fido",
                "breed": Breed.GOLDEN_RETRIEVER,
                "birthday": "01/01/2015",
                "weight": "10.50",
            },
        )
        pet = Pet.objects.get(pk=1)
        pet.update_pet({
                "name": "Fido",
                "breed": Breed.GOLDEN_RETRIEVER,
                "birthday": "01/01/2015",
                "weight": "Con este peso no deberia updatear",
                })
        pet_updated = Pet.objects.get(pk=1)
        self.assertEqual(pet_updated.weight, Decimal("10.50"))



    def test_create_pet_with_error_weight(self):
        """"
        Se crea una mascota y se verifica que se haya creado correctamente
        """
        # se crea una mascota
        Pet.save_pet(
            {
                "name": "Fido",
                "breed": Breed.GOLDEN_RETRIEVER,
                "birthday": "01/01/2015",
                "weight": "dsadsadsad",
            },
        )
        # se verifica que la mascota se haya creado correctamente
        pets = Pet.objects.all()
        # se verifica que no haya una mascota
        self.assertEqual(len(pets), 0)

    def test_create_pet_with_empty_weight(self):
        """"
        Se crea una mascota y se verifica que se haya creado correctamente
        """
        # se crea una mascota
        Pet.save_pet(
            {
                "name": "Fido",
                "breed": Breed.GOLDEN_RETRIEVER,
                "birthday": "01/01/2015",
                "weight": "",
            },
        )
        # se verifica que la mascota se haya creado correctamente
        pets = Pet.objects.all()
        # se verifica que no haya una mascota
        self.assertEqual(len(pets), 0)

    def test_create_pet_with_error_breed(self):
        """"
        Se crea una mascota y se verifica que se haya creado correctamente
        """
        # se crea una mascota
        Pet.save_pet(
            {
                "name": "Fido",
                "breed": "Con esta raza no va a funcionar",
                "birthday": "01/01/2015",
                "weight": "1000",
            },
        )
        # se verifica que la mascota se haya creado correctamente
        pets = Pet.objects.all()
        # se verifica que no haya una mascota
        self.assertEqual(len(pets), 0)

    def test_create_pet_with_empty_breed(self):
        """"
        Se crea una mascota y se verifica que se haya creado correctamente
        """
        # se crea una mascota
        Pet.save_pet(
            {
                "name": "Fido",
                "breed": "",
                "birthday": "01/01/2015",
                "weight": "1000",
            },
        )
        # se verifica que la mascota se haya creado correctamente
        pets = Pet.objects.all()
        # se verifica que no haya una mascota
        self.assertEqual(len(pets), 0)


class VetModelTest(TestCase):
    """Modelo de test para la clase Vet en app.models.py"""
    def test_can_create_and_get_vet(self):
        """"
        Se crea un veterinario y se verifica que se haya creado correctamente
        """
        Vet.save_vet(
            {
                "name": "Juan Sebastian Veron",
                "email": "brujita75@hotmail.com",
                "phone": "2215552324",
                "speciality": Speciality.GENERAL,
            },
        )
        vets = Vet.objects.all()
        self.assertEqual(len(vets), 1)

        self.assertEqual(vets[0].name, "Juan Sebastian Veron")
        self.assertEqual(vets[0].email, "brujita75@hotmail.com")
        self.assertEqual(vets[0].phone, "2215552324")
        self.assertEqual(vets[0].speciality, Speciality.GENERAL)

    def test_cant_create_and_get_vet_empty_speciality(self):
        """"
        Se crea un veterinario y se verifica que se haya creado correctamente
        """
        Vet.save_vet(
            {
                "name": "Juan Sebastian Veron",
                "email": "brujita75@hotmail.com",
                "phone": "2215552324",
            },
        )
        vets = Vet.objects.all()
        self.assertEqual(len(vets), 0)



    def test_can_update_vet(self):
        """"
        Se crea un veterinario y se verifica que se haya creado correctamente
        """
        Vet.save_vet(
            {
                "name": "Juan Sebastian Veron",
                "email": "brujita75@hotmail.com",
                "phone": "2215552324",
                "speciality": Speciality.CARDIOLOGO,
            },
        )
        vet = Vet.objects.get(pk=1)

        self.assertEqual(vet.speciality, Speciality.CARDIOLOGO)

        vet.update_vet(
            {
                "name": "Juan Sebastian Veron",
                "email": "brujita75@hotmail.com",
                "phone": "2215552324",
                "speciality": Speciality.DERMATOLOGO,
            },
        )
        vet_updated = Vet.objects.get(pk=1)

        self.assertEqual(vet_updated.speciality, Speciality.DERMATOLOGO)

    def test_update_vet_with_error_speciality(self):
        """"
        Se crea un veterinario y se verifica que se haya creado correctamente
        """
        Vet.save_vet(
            {
                "name": "Juan Sebastian Veron",
                "email": "brujita75@hotmail.com",
                "phone": "2215552324",
                "speciality": Speciality.DERMATOLOGO,
            },
        )
        vet = Vet.objects.get(pk=1)

        self.assertEqual(vet.speciality, Speciality.DERMATOLOGO)

        vet.update_vet(
            {
                "name": "Juan Sebastian Veron",
                "email": "brujita75@hotmail.com",
                "phone": "2215552324",
                "speciality": "esta especialidad no existe y no deberia guardarlo",
            },
        )

        vet_updated = Vet.objects.get(pk=1)
        # como no se actualizo la especialidad deberia ser la misma
        self.assertEqual(vet_updated.speciality, Speciality.DERMATOLOGO)

    def test_update_vet_with_error_speciality_empty(self):
        """"
        Se crea un veterinario y se verifica que se haya creado correctamente
        """
        Vet.save_vet(
            {
                "name": "Juan Sebastian Veron",
                "email": "brujita75@hotmail.com",
                "phone": "2215552324",
                "speciality": Speciality.DERMATOLOGO,
            },
        )
        vet = Vet.objects.get(pk=1)

        self.assertEqual(vet.speciality, Speciality.DERMATOLOGO)

        vet.update_vet(
            {
                "name": "Juan Sebastian Veron",
                "email": "brujita75@hotmail.com",
                "phone": "2215552324",
                "speciality": "",
            },
        )

        vet_updated = Vet.objects.get(pk=1)
        # como no se actualizo la especialidad deberia ser la misma
        self.assertEqual(vet_updated.speciality, Speciality.DERMATOLOGO)

    def test_update_vet_with_error_speciality_none(self):
        """"
        Se crea un veterinario y se verifica que se haya creado correctamente
        """
        Vet.save_vet(
            {
                "name": "Juan Sebastian Veron",
                "email": "brujita75@hotmail.com",
                "phone": "2215552324",
                "speciality": Speciality.DERMATOLOGO,
            },
        )
        vet = Vet.objects.get(pk=1)

        self.assertEqual(vet.speciality, Speciality.DERMATOLOGO)

        vet.update_vet(
            {
                "name": "Juan Sebastian Veron",
                "email": "brujita75@hotmail.com",
                "phone": "2215552324",
                #no mando la especialidad
            },
        )

        vet_updated = Vet.objects.get(pk=1)
        # como no se actualizo la especialidad deberia ser la misma
        self.assertEqual(vet_updated.speciality, Speciality.DERMATOLOGO)

class ProviderModelTest(TestCase):
    """Modelo de test para la clase Provider en app.models.py"""
    def test_can_create_and_get_provider(self):
        """"
        Se crea un proveedor y se verifica que se haya creado correctamente
        """
        Provider.save_provider(
            {
                "name": "Valentina",
                "email": "estudiantes@gmail.com",
                "direccion": "12 y 47",
            },
        )
        providers = Provider.objects.all()
        self.assertEqual(len(providers), 1)

        self.assertEqual(providers[0].name, "Valentina")
        self.assertEqual(providers[0].email, "estudiantes@gmail.com")
        self.assertEqual(providers[0].direccion, "12 y 47")

    def test_can_update_provider(self):
        """"
        Se crea un proveedor y se verifica que se haya creado correctamente
        """
        Provider.save_provider(
            {
                "name": "Valentina",
                "email": "estudiantes@gmail.com",
                "direccion": "casa",
            },
        )
        provider = Provider.objects.get(pk=1)

        self.assertEqual(provider.direccion, "casa")

        provider.update_provider({
                "name": "Valentina",
                "email": "estudiantes@gmail.com",
                "direccion": "facultad",
            })

        provider_updated = Provider.objects.get(pk=1)

        self.assertEqual(provider_updated.direccion, "facultad")

    def test_update_provider_with_error(self):
        """"
        Se crea un proveedor y se verifica que se haya creado correctamente
        """
        Provider.save_provider(
            {
                "name": "Valentina",
                "email": "estudiantes@gmail.com",
                "direccion": "12 y 47",
            },
        )
        provider = Provider.objects.get(pk=1)

        self.assertEqual(provider.direccion, "12 y 47")

        provider.update_provider({"direccion": ""})

        provider_updated = Provider.objects.get(pk=1)

        self.assertEqual(provider_updated.direccion, "12 y 47")

    def test_provider_adress_cannot_be_empty(self):
        """"
        Se crea un proveedor y se verifica que se haya creado correctamente
        """
        valid, errors = Provider.save_provider({
            "name": "Valentina",
            "email": "estudiantes@gmail.com",
            "direccion": "",
        })
        self.assertFalse(valid)
        self.assertIn("direccion", errors)
        self.assertEqual(errors["direccion"], "Por favor ingrese una direccion")
