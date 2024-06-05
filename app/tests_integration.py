from decimal import Decimal

from django.shortcuts import reverse
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


class HomePageTest(TestCase):
    """testea la pagina de inicio y el template que se va a usar."""
    def test_use_home_template(self):
        """
        test para verificar que la pagina de inicio use el template correcto
        """
        response = self.client.get(reverse("home"))
        self.assertTemplateUsed(response, "home.html")


class ClientsTest(TestCase):
    """testea la pagina de clientes y la creacion de un cliente."""
    def test_repo_use_repo_template(self):
        """"
        test para verificar que la pagina de inicio de clientes use el template correcto
        """
        response = self.client.get(reverse("clients_repo"))
        self.assertTemplateUsed(response, "clients/repository.html")

    def test_repo_display_all_clients(self):
        """"
        test para verificar que se muestren todos los clientes en la pagina de inicio
        """
        response = self.client.get(reverse("clients_repo"))
        self.assertTemplateUsed(response, "clients/repository.html")

    def test_form_use_form_template(self):
        """"
        test para verificar que el formulario de clientes use el template correcto
        """
        response = self.client.get(reverse("clients_form"))
        self.assertTemplateUsed(response, "clients/form.html")

    def test_can_create_client(self):
        """"
        test para verificar que se pueda crear un cliente
        """
        response = self.client.post(
            reverse("clients_form"),
            data={
                "name": "Juan Sebastian Veron",
                "phone": "54221555232",
                "email": "brujita75@vetsoft.com",
                "city": CityEnum.LA_PLATA,
            },
        )
        clients = Client.objects.all()
        self.assertEqual(len(clients), 1)
        self.assertEqual(clients[0].name, "Juan Sebastian Veron")
        self.assertEqual(clients[0].phone, 54221555232)
        self.assertEqual(clients[0].email, "brujita75@vetsoft.com")
        self.assertEqual(clients[0].city, "La Plata")

        self.assertRedirects(response, reverse("clients_repo"))



    def test_validation_errors_create_client(self):
        """"
        test para verificar que se muestren los errores de validacion al crear un cliente
        """
        response = self.client.post(
            reverse("clients_form"),
            data={},
        )

        self.assertContains(response, "Por favor ingrese un nombre")
        self.assertContains(response, "Por favor ingrese un teléfono")
        self.assertContains(response, "Por favor ingrese un email")
        self.assertContains(response, "Por favor ingrese una ciudad")

    def test_validation_errors_create_client_wrong_phone(self):
        """"
        test para verificar que se muestren los errores de validacion al crear un cliente con telefono incorrecto
        """
        response = self.client.post(
            reverse("clients_form"),
            data={
                "name": "Juan Sebastian Veron",
                "phone": "221555232",
                "email": "brujita75@vetsoft.com",
                "city": CityEnum.LA_PLATA,
            },
        )

        self.assertContains(response, "Por favor ingrese un teléfono válido")

    def test_validation_errors_create_client_wrong_city(self):
        """"
        test para verificar que se muestren los errores de validacion al crear un cliente con telefono incorrecto
        """
        response = self.client.post(
            reverse("clients_form"),
            data={
                "name": "Juan Sebastian Veron",
                "phone": "54221555232",
                "city": "Esta ciudad no existe",
                "email": "brujita75@vetsoft.com",
            },
        )

        self.assertContains(response, "Ciudad no válida")

    def test_validation_create_with_invalid_name(self):
        """"
        test para verificar que se muestre un error si el nombre es invalido
        """
        response = self.client.post(
            reverse("clients_form"),
            data={
                "name": "Juan132",
                "phone": "54221555232",
                "city": CityEnum.LA_PLATA,
                "email": "brujita75@vetsoft.com",
            },
        )

        self.assertContains(response, "El nombre solo debe contener letras y espacios")




    def test_should_response_with_404_status_if_client_doesnt_exists(self):
        """"
        test para verificar que se muestre un error 404 si el cliente no existe
        """
        response = self.client.get(reverse("clients_edit", kwargs={"id": 100}))
        self.assertEqual(response.status_code, 404)

    def test_validation_create_with_invalid_email(self):
        """"
        test para verificar que se muestre un error si el email es invalido
        """
        response = self.client.post(
            reverse("clients_form"),
            data={
                "name": "Juan Sebastian Veron",
                "phone": "54221555232",
                "city": CityEnum.LA_PLATA,
                "email": "brujita75",
            },
        )

        self.assertContains(response, "Por favor ingrese un email valido")

    def test_edit_user_with_valid_data_test(self):
        """"
        test para editar un cliente con datos validos.
        """
        client = Client.objects.create(
            name="Guido Carrillo",
            city=CityEnum.LA_PLATA,
            phone="54221555232",
            email="guido@vetsoft.com",
        )

        response = self.client.post(
            reverse("clients_form"),
              data={
                "id": client.id,
                "name": "Juan Sebastian Veron",
                "phone": "54221123123",
                "email": "brujita71@vetsoft.com",
                "city": CityEnum.BERISSO,
            },
        )

        # redirect after post
        self.assertEqual(response.status_code, 302)

        editedClient = Client.objects.get(pk=client.id)
        self.assertEqual(editedClient.name, "Juan Sebastian Veron")
        self.assertEqual(editedClient.email, "brujita71@vetsoft.com")
        self.assertEqual(editedClient.phone, 54221123123)
        self.assertEqual(editedClient.city, CityEnum.BERISSO)


    def test_edit_user_with_invalid_data_test_phone(self):
        """"
        test para editar un cliente con datos validos y chequeo de telefono
        """
        client = Client.objects.create(
            name="Guido Carrillo",
            city=CityEnum.LA_PLATA,
            phone="54221555232",
            email="brujita75@vetsoft.com",
        )

        self.client.post(
            reverse("clients_form"),
              data={
                "id": client.id,
                "name": "Juan Sebastian Veron",
                "phone": "221123123",
                "email": "brujita71@vetsoft.com",
                "city": CityEnum.LA_PLATA,
            },
        )

        # redirect after post
        editedClient = Client.objects.get(pk=client.id)
        self.assertEqual(editedClient.phone, 54221555232)

    def test_invalid_phone_format_on_client_form(self):
        """
        Verifica que no se permitan valores no numericos en phone
        """

        client = Client.objects.create(
            name="Guido Carrillo",
            phone="54221555232",
            email="brujita75@hotmail.com",
        )

        self.client.post(
            reverse("clients_form"),
            data={
                "id": client.id,
                "name": "Juan Sebastian Veron",
                "phone": "54 1134563456",  #Agrego espacio para que ya no sea un int
                "email": "brujita71@gmail.com",
            },
        )

        edited_client = Client.objects.get(pk=client.id)
        self.assertEqual(edited_client.phone, 54221555232)

    def test_edit_user_with_invalid_data_test_email(self):
        """"
        test para editar un cliente con datos validos y chequeo de email
        """
        client = Client.objects.create(
            name="Guido Carrillo",
            city=CityEnum.LA_PLATA,
            phone="54221555232",
            email="brujita75@vetsoft.com",
        )

        self.client.post(
            reverse("clients_form"),
              data={
                "id": client.id,
                "name": "Juan Sebastian Veron",
                "phone": "54221555232",
                "city": CityEnum.ENSENADA,
                "email": "brujita71@hotmail.com",
            },
        )

        # redirect after post
        editedClient = Client.objects.get(pk=client.id)
        self.assertEqual(editedClient.email, "brujita75@vetsoft.com")

    def test_edit_user_with_invalid_data_test_city(self):
        """"
        test para editar un cliente con datos validos y chequeo de ciudad
        """
        client = Client.objects.create(
            name="Guido Carrillo",
            city=CityEnum.LA_PLATA,
            phone="54221555232",
            email="brujita75@vetsoft.com",
        )


        self.client.post(
            reverse("clients_form"),
              data={
                "id": client.id,
                "name": "Juan Sebastian Veron",
                "phone": "54221123123",
                "city": "esta ciudad no existe",
                "email": "brujita75@vetsoft.com",
            },
        )

        # redirect after post
        editedClient = Client.objects.get(pk=client.id)
        self.assertEqual(editedClient.city, CityEnum.LA_PLATA)


# Test Producto
class ProductsTest(TestCase):
    """Testea la pagina de productos y la creacion de un producto."""
    def test_repo_use_repo_template(self):
        """"
        test para verificar que la pagina de inicio de productos use el template correcto
        """
        response = self.client.get(reverse("products_repo"))
        self.assertTemplateUsed(response, "products/repository.html")

    def test_repo_display_all_products(self):
        """"
        test para verificar que se muestren todos los productos en la pagina de inicio
        """
        response = self.client.get(reverse("products_repo"))
        self.assertTemplateUsed(response, "products/repository.html")

    def test_form_use_form_template(self):
        """"
        test para verificar que el formulario de productos use el template correcto
        """
        response = self.client.get(reverse("products_form"))
        self.assertTemplateUsed(response, "products/form.html")

    def test_can_create_product(self):
        """"
        test para verificar que se pueda crear un producto
        """
        response = self.client.post(
            reverse("products_form"),
            data={
                "name": "DogChow",
                "type": "Perro adulto",
                "price": "10400.50",
            },
        )
        products = Product.objects.all()
        self.assertEqual(len(products), 1)

        self.assertEqual(products[0].name, "DogChow")
        self.assertEqual(products[0].type, "Perro adulto")
        self.assertEqual(products[0].price, 10400.50)

        self.assertRedirects(response, reverse("products_repo"))

    def test_validation_errors_create_product(self):
        """"
        test para verificar que se muestren los errores de validacion al crear un producto
        """
        response = self.client.post(
            reverse("products_form"),
            data={},
        )

        self.assertContains(response, "Por favor ingrese el nombre del producto")
        self.assertContains(response, "Por favor ingrese el tipo de producto")
        self.assertContains(response, "Por favor ingrese un precio válido")

    def test_should_response_with_404_status_if_product_doesnt_exists(self):
        """"
        test para verificar que se muestre un error 404 si el producto no existe
        """
        response = self.client.get(reverse("products_edit", kwargs={"id": 100}))
        self.assertEqual(response.status_code, 404)

    def test_validation_invalid_price(self):
        """"
        test para verificar que se muestre un error si el precio es invalido
        """
        response = self.client.post(
            reverse("products_form"),
            data={
                "name": "DogChow",
                "type": "Perro adulto",
                "price": "10 mil pesos",
            },
        )

        self.assertContains(response, "Por favor ingrese un precio válido")

    def test_edit_user_with_valid_data(self):
        """"
        test para editar un producto con datos validos
        """
        product = Product.objects.create(
            name="DogChow",
            type="Perro adulto",
            price="10400.50",
        )

        response = self.client.post(
            reverse("products_form"),
            data={
                "id": product.id,
                "name": "DogChow",
                "type": "Perro adulto",
                "price": "14400.50",
            },
        )

        # redirect after post
        self.assertEqual(response.status_code, 302)

        editedProduct = Product.objects.get(pk=product.id)
        self.assertEqual(editedProduct.name, "DogChow")
        self.assertEqual(editedProduct.type, product.type)
        self.assertEqual(editedProduct.price,  14400.50)
        self.assertNotEqual(editedProduct.price, product.price)
class MedicinesTest(TestCase):
    """Testea la pagina de medicamentos y la creacion de un medicamento."""
    def test_repo_use_repo_template(self):
        """"
        test para verificar que la pagina de inicio de medicamentos use el template correcto
        """
        response = self.client.get(reverse("medicines_repo"))
        self.assertTemplateUsed(response, "medicines/repository.html")

    def test_repo_display_all_medicines(self):
        """"
        test para verificar que se muestren todos los medicamentos en la pagina de inicio
        """
        Medicine.objects.create(name="Ivermectina", description="ectoparásitos y endoparásitos", dose=5)
        Medicine.objects.create(name="Frontline ", description="pulgas y piojos", dose=3)

        response = self.client.get(reverse("medicines_repo"))
        self.assertTemplateUsed(response, "medicines/repository.html")
        self.assertContains(response, "Ivermectina")
        self.assertContains(response, "Frontline ")

    def test_form_use_form_template(self):
        """"
        test para verificar que el formulario de medicamentos use el template correcto
        """
        response = self.client.get(reverse("medicines_form"))
        self.assertTemplateUsed(response, "medicines/form.html")

    def test_can_create_medicine(self):
        """"
        test para verificar que se pueda crear un medicamento
        """
        response = self.client.post(
            reverse("medicines_form"),
            data={
                "name": "Ivermectina",
                "description": "ectoparásitos y endoparásitos",
                "dose": 5,
            },
        )
        medicines = Medicine.objects.all()
        self.assertEqual(len(medicines), 1)
        self.assertEqual(medicines[0].name, "Ivermectina")
        self.assertEqual(medicines[0].description, "ectoparásitos y endoparásitos")
        self.assertEqual(medicines[0].dose, 5)
        self.assertRedirects(response, reverse("medicines_repo"))

    def test_validation_errors_create_medicine(self):
        """"
        test para verificar que se muestren los errores de validacion al crear un medicamento
        """
        response = self.client.post(reverse("medicines_form"), data={})
        self.assertContains(response, "Por favor ingrese un nombre")
        self.assertContains(response, "Por favor ingrese una descripción")
        self.assertContains(response, "Por favor ingrese una dosis")

    def test_validation_invalid_dose_is_greater_than_10(self):
        """
        test para verificar que se muestre un error si la dosis es mayor a 10
        """
        response = self.client.post(
            reverse("medicines_form"),
            data={
                "name": "Ivermectina",
                "description": "ectoparásitos y endoparásitos",
                "dose": 11,
            },
        )
        self.assertContains(response, "Por favor ingrese una dosis entre 1 y 10")

    def test_validation_dose_must_be_numeric(self):
        """"
        test para verificar que se muestre un error si la dosis no es numerica
        """
        response = self.client.post(
            reverse("medicines_form"),
            data={
                "name": "Ivermectina",
                "description": "ectoparásitos y endoparásitos",
                "dose": "abc",
            },
        )
        self.assertContains(response, "Por favor ingrese una dosis válida")

    def test_validation_dose_is_less_than_1(self):
        """"
        test para verificar que se muestre un error si la dosis es menor a 1
        """
        response = self.client.post(
            reverse("medicines_form"),
            data={
                "name": "Ivermectina",
                "description": "ectoparásitos y endoparásitos",
                "dose": 0,
            },
        )
        self.assertContains(response, "Por favor ingrese una dosis entre 1 y 10")



    def test_should_response_with_404_status_if_medicine_doesnt_exist(self):
        """"
        test para verificar que se muestre un error 404 si el medicamento no existe
        """
        response = self.client.get(reverse("medicines_edit", kwargs={"id": 100}))
        self.assertEqual(response.status_code, 404)

    def test_can_delete_medicine(self):
        """"
        test para verificar que se pueda eliminar un medicamento
        """
        medicine = Medicine.objects.create(
            name="Ivermectina", description="ectoparásitos y endoparásitos", dose=5,
        )
        response = self.client.post(reverse("medicines_delete"), data={"medicine_id": medicine.id})
        self.assertEqual(response.status_code, 302)

        medicines = Medicine.objects.all()
        self.assertEqual(len(medicines), 0)


    def test_edit_medicine_with_valid_data(self):
        """"
        test para editar un medicamento con datos validos
        """
        medicine = Medicine.objects.create(
            name="Ivermectina", description="ectoparásitos y endoparásitos", dose=5,
        )

        response = self.client.post(
            reverse("medicines_edit", kwargs={"id": medicine.id}),
            data={
                "id": medicine.id,
                "name": "Frontline ",
                "description": "pulgas y piojos",
                "dose": 3,
            },
        )
        self.assertEqual(response.status_code, 302)

        edited_medicine = Medicine.objects.get(pk=medicine.id)
        self.assertEqual(edited_medicine.name, "Frontline ")
        self.assertEqual(edited_medicine.description, "pulgas y piojos")
        self.assertEqual(edited_medicine.dose, 3)




class PetsTest(TestCase):
    """Testea la pagina de mascotas y la creacion de una mascota."""
    # defino el test de la pagina de inicio para mascota y el template que se va a usar
    # esto es para chequear que la pagina de inicio de mascotas use el template correcto
    def test_repo_use_repo_template(self):
        """"
        test para verificar que la pagina de inicio de mascotas use el template correcto
        """
        response = self.client.get(reverse("pets_repo"))
        self.assertTemplateUsed(response, "pets/repository.html")

    # defino el test para ver si se muestran todas las mascotas en la pagina de inicio
    def test_repo_display_all_pets(self):
        """"
        test para verificar que se muestren todas las mascotas en la pagina de inicio
        """
        response = self.client.get(reverse("pets_repo"))
        self.assertTemplateUsed(response, "pets/repository.html")

    # defino el test para ver si se usa el template correcto en el formulario de mascotas
    def test_form_use_form_template(self):
        """"
        test para verificar que el formulario de mascotas use el template correcto
        """
        response = self.client.get(reverse("pets_form"))
        self.assertTemplateUsed(response, "pets/form.html")


    # defino el test para crear una mascota
    def test_can_create_pet(self):
        """"
        test para verificar que se pueda crear una mascota
        """
        response = self.client.post(
            reverse("pets_form"),
            data={
                "name": "Fido",
                "breed": Breed.GOLDEN_RETRIEVER,
                "birthday": "01/01/2015",
                "weight": "10.50",
            },
        )
        # traigo todas las mascotas
        pets = Pet.objects.all()
        # verifico que se haya creado una mascota con los datos correctos
        self.assertEqual(len(pets), 1)
        self.assertEqual(pets[0].name, "Fido")
        self.assertEqual(pets[0].breed, "Golden Retriever")
        self.assertEqual(pets[0].birthday.strftime("%d/%m/%Y"), "01/01/2015")
        self.assertEqual(pets[0].weight, Decimal("10.50"))
        # verifico que se redirija a la pagina de inicio de mascotas
        self.assertRedirects(response, reverse("pets_repo"))

    # creo un test para verificar si la mascota no existe
    def test_should_response_with_404_status_if_pet_doesnt_exists(self):
        """"
        test para verificar que se muestre un error 404 si la mascota no existe
        """
        response = self.client.get(reverse("pets_edit", kwargs={"id": 100}))
        self.assertEqual(response.status_code, 404)

    # creo un test para verificar si el peso de la mascota es invalido
    def test_validation_invalid_weight(self):
        """"
        test para verificar que se muestre un error si el peso es invalido
        """
        response = self.client.post(
            reverse("pets_form"),
            data={
                "name": "Fido",
                "breed": Breed.GOLDEN_RETRIEVER,
                "birthday": "01/01/2015",
                "weight": "invalid",
            },
        )
        # verifico que se muestre el error de validacion
        self.assertContains(response, "El peso debe ser un número positivo con hasta dos decimales.")

    # creo un test para verificar si el peso de la mascota es invalido
    def test_validation_invalid_breed(self):
        """"
        test para verificar que se muestre un error si la raza es invalida
        """
        response = self.client.post(
            reverse("pets_form"),
            data={
                "name": "Fido",
                "breed": "No deberia de funcionar",
                "birthday": "01/01/2015",
                "weight": "1000.00",
            },
        )
        # verifico que se muestre el error de validacion
        self.assertContains(response, "La raza no es válida.")

    def test_validation_errors_create_pet(self):
        """"
        test para verificar que se muestren los errores de validacion al crear una mascota
        """
        response = self.client.post(
            reverse("pets_form"),
            data={},  # Asegúrate de que este dict está vacío si quieres probar la validación.
        )
        self.assertContains(response, "El nombre es requerido.")
        self.assertContains(response, "La raza es requerida.")
        self.assertContains(response, "La fecha de nacimiento es requerida.")
        self.assertContains(response, "El peso es requerido.")

    #  test para editar una mascota con datos validos
    def test_edit_pet_with_valid_data(self):
        """"
        test para editar una mascota con datos validos
        """
        # Creación de una mascota con datos iniciales.
        pet = Pet.objects.create(
            name="Fido",
            breed=Breed.GOLDEN_RETRIEVER,
            birthday="2015-01-01",
            weight="10.50",
        )

        # Intento de editar la mascota enviando datos en el formato correcto.
        response = self.client.post(
            reverse("pets_edit", kwargs={"id": pet.id}),
            data ={
                "id": pet.id,
                "name": "cambio",
                "breed": Breed.BEAGLE,
                "birthday": "01/01/2014",  # Formato correcto de fecha.
                "weight": "1212",  # Peso que se intenta establecer.
            },
        )

        self.assertEqual(response.status_code, 302)

        # Obtención de la mascota editada para verificación.
        editedPet = Pet.objects.get(pk=pet.id)

        # Verificaciones para asegurar que los datos no han cambiado incorrectamente.
        self.assertNotEqual(editedPet.name, pet.name)
        self.assertNotEqual(editedPet.breed, pet.breed)
        self.assertNotEqual(editedPet.birthday, pet.birthday)
        self.assertNotEqual(editedPet.weight, pet.weight)
        self.assertEqual(editedPet.weight, Decimal("1212.00"))  # Corrección al valor correcto de peso esperado.


class VetsTest(TestCase):
    """Testea la pagina de veterinarios y la creacion de un veterinario."""
    def test_repo_use_repo_template_vet(self):
        """"
        test para verificar que la pagina de inicio de veterinarios use el template correcto
        """
        response = self.client.get(reverse("vets_repo"))
        self.assertTemplateUsed(response, "vets/repository.html")

    def test_repo_display_all_vets(self):
        """"
        test para verificar que se muestren todos los veterinarios en la pagina de inicio
        """
        response = self.client.get(reverse("vets_repo"))
        self.assertTemplateUsed(response, "vets/repository.html")

    def test_form_use_form_template_vet(self):
        """"
        test para verificar que el formulario de veterinarios use el template correcto
        """
        response = self.client.get(reverse("vets_form"))
        self.assertTemplateUsed(response, "vets/form.html")

    def test_can_create_vet(self):
        """"
        test para verificar que se pueda crear un veterinario
        """
        response = self.client.post(
            reverse("vets_form"),
            data={
                "name": "Juan Sebastian Veron",
                "email": "brujita75@hotmail.com",
                "phone": "2215552324",
                "speciality": Speciality.DERMATOLOGO,
            },
        )
        vets = Vet.objects.all()
        self.assertEqual(len(vets), 1)

        self.assertEqual(vets[0].name, "Juan Sebastian Veron")
        self.assertEqual(vets[0].email, "brujita75@hotmail.com")
        self.assertEqual(vets[0].phone, "2215552324")
        self.assertEqual(vets[0].speciality, Speciality.DERMATOLOGO)

        self.assertRedirects(response, reverse("vets_repo"))

    def test_validation_errors_create_vet(self):
        """"
        test para verificar que se muestren los errores de validacion al crear un veterinario
        """
        response = self.client.post(
            reverse("vets_form"),
            data={},
        )

        self.assertContains(response, "Por favor ingrese un nombre")
        self.assertContains(response, "Por favor ingrese un teléfono")
        self.assertContains(response, "Por favor ingrese un email")
        self.assertContains(response, "Por favor ingrese una especialidad")

    def test_should_response_with_404_status_if_vet_doesnt_exists(self):
        """
        test para verificar que se muestre un error 404 si el veterinario no existe
        """
        response = self.client.get(reverse("vets_edit", kwargs={"id": 1000}))
        self.assertEqual(response.status_code, 404)

    def test_validation_create_with_invalid_speciality(self):
        """
        test para verificar que se muestre un error si la especialidad no es valida
        """
        response = self.client.post(
            reverse("vets_form"),
            data={
                "name": "Juan Sebastian Veron",
                "email": "brujita75@hotmail.com",
                "phone": "2215552324",
                "speciality": "esta especialidad no existe",
            },
        )
        self.assertContains(response, "Especialidad no válida")




    def test_validation_create_with_invalid_speciality_none(self):
        """"
        test para verificar que se muestre un error si la especialidad no es valida
        """
        response = self.client.post(
            reverse("vets_form"),
            data={
                "name": "Juan Sebastian Veron",
                "email": "brujita75@hotmail.com",
                "phone": "2215552324",
            },
        )
        self.assertContains(response, "Por favor ingrese una especialidad")

    def test_validation_create_with_invalid_speciality_empty(self):
        """"
        test para verificar que se muestre un error si la especialidad no es valida
        """
        response = self.client.post(
            reverse("vets_form"),
            data={
                "name": "Juan Sebastian Veron",
                "email": "brujita75@hotmail.com",
                "phone": "2214202798",
                "speciality": "",
            },
        )
        self.assertContains(response, "Por favor ingrese una especialidad")

    def test_edit_vet_with_valid_data(self):
        """"
        test para editar un veterinario con datos validos
        """
        vet = Vet.objects.create(
            name="Juan Sebastián Veron",
            email="brujita75@hotmail.com",
            phone="2215552324",
            speciality = Speciality.CARDIOLOGO,
        )

        response = self.client.post(
            reverse("vets_form"),
            data={
                "id": vet.id,
                "name": "Juan Sebastian Veron",
                "email": "brujita75@hotmail.com",
                "phone": "2215552324",
                "speciality": Speciality.DERMATOLOGO,
            },
        )

        # redirect after post
        self.assertEqual(response.status_code, 302)

        editedVet = Vet.objects.get(pk=vet.id)
        self.assertEqual(editedVet.name, "Juan Sebastian Veron")
        self.assertEqual(editedVet.email, vet.email)
        self.assertEqual(editedVet.phone, vet.phone)
        self.assertEqual(editedVet.speciality, Speciality.DERMATOLOGO)


    def test_edit_vet_with_invalid_data_speciality_none(self):
        """"
        test para editar un veterinario con datos invalidos
        """
        vet = Vet.objects.create(
            name="Juan Sebastián Veron",
            email="brujita75@hotmail.com",
            phone="2215552324",
            speciality = Speciality.CARDIOLOGO,
        )

        response = self.client.post(
            reverse("vets_form"),
            data={
                "id": vet.id,
                "name": "Juan Sebastian Veron",
                "email": "brujita75@hotmail.com",
                "phone": "2215552324",
            },
        )

        # redirect after post
        self.assertEqual(response.status_code, 200)

        editedVet = Vet.objects.get(pk=vet.id)
        self.assertEqual(editedVet.name, vet.name)
        self.assertEqual(editedVet.email, vet.email)
        self.assertEqual(editedVet.phone, vet.phone)
        self.assertEqual(editedVet.speciality, Speciality.CARDIOLOGO)
        self.assertNotEqual(editedVet.speciality, Speciality.DERMATOLOGO)

    def test_edit_vet_with_invalid_data_speciality_empty(self):
        """"
        test para editar un veterinario con datos invalidos
        """
        vet = Vet.objects.create(
            name="Juan Sebastián Veron",
            email="brujita75@hotmail.com",
            phone="2215552324",
            speciality = Speciality.CARDIOLOGO,
        )

        response = self.client.post(
            reverse("vets_form"),
            data={
                "id": vet.id,
                "name": "Juan Sebastian Veron",
                "email": "brujita75@hotmail.com",
                "phone": "2215552324",
                "speciality": "",
            },
        )

        # redirect after post
        self.assertEqual(response.status_code, 200)

        editedVet = Vet.objects.get(pk=vet.id)
        self.assertEqual(editedVet.name, vet.name)
        self.assertEqual(editedVet.email, vet.email)
        self.assertEqual(editedVet.phone, vet.phone)
        self.assertEqual(editedVet.speciality, Speciality.CARDIOLOGO)
        self.assertNotEqual(editedVet.speciality, Speciality.DERMATOLOGO)

    def test_edit_vet_with_invalid_data_speciality(self):
        """"
        test para editar un veterinario con datos invalidos
        """
        vet = Vet.objects.create(
            name="Juan Sebastián Veron",
            email="brujita75@hotmail.com",
            phone="2215552324",
            speciality = Speciality.CARDIOLOGO,
        )

        response = self.client.post(
            reverse("vets_form"),
            data={
                "id": vet.id,
                "name": "Juan Sebastian Veron",
                "email": "brujita75@hotmail.com",
                "phone": "2215552324",
                "speciality": "esta especialidad no existe, no deberia actualizar",
            },
        )

        # redirect after post
        self.assertEqual(response.status_code, 200)

        editedVet = Vet.objects.get(pk=vet.id)
        self.assertEqual(editedVet.name, vet.name)
        self.assertEqual(editedVet.email, vet.email)
        self.assertEqual(editedVet.phone, vet.phone)
        self.assertEqual(editedVet.speciality, Speciality.CARDIOLOGO)
        self.assertNotEqual(editedVet.speciality, Speciality.DERMATOLOGO)

##############################

class ProvidersTest(TestCase):
    """Testea la pagina de proveedores y la creacion de un proveedor de servicios."""
    def test_repo_use_repo_template(self):
        """"
        test para verificar que la pagina de inicio de proveedores use el template correcto
        """
        response = self.client.get(reverse("providers_repo"))
        self.assertTemplateUsed(response, "providers/repository.html")

    def test_repo_display_all_providers(self):
        """"
        test para verificar que se muestren todos los proveedores en la pagina de inicio
        """
        Provider.objects.create(name="Valentina", email="estudiantes@gmail.com", direccion="12 y 47")
        Provider.objects.create(name="Faustina", email="boca@gmail.com", direccion="12 y 50")

        response = self.client.get(reverse("providers_repo"))
        self.assertTemplateUsed(response, "providers/repository.html")
        self.assertContains(response, "Valentina")
        self.assertContains(response, "Faustina")

    def test_form_use_form_template(self):
        """"
        test para verificar que el formulario de proveedores use el template correcto
        """
        response = self.client.get(reverse("providers_form"))
        self.assertTemplateUsed(response, "providers/form.html")

    def test_can_create_provider(self):
        """"
        test para verificar que se pueda crear un proveedor
        """
        response = self.client.post(
            reverse("providers_form"),
            data={
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
        self.assertRedirects(response, reverse("providers_repo"))

    def test_validation_errors_create_provider(self):
        """"
        test para verificar que se muestren los errores de validacion al crear un proveedor
        """
        response = self.client.post(reverse("providers_form"), data={})
        self.assertContains(response, "Por favor ingrese un nombre")
        self.assertContains(response, "Por favor ingrese un email")
        self.assertContains(response, "Por favor ingrese una direccion")


    def test_validation_invalid_email(self):
        """
        test para verificar que se muestre un error si el email es invalido
        """
        response = self.client.post(
            reverse("providers_form"),
            data={
                "name": "Valentina",
                "email": "estudiantes",
                "direccion": "12 y 47",
            },
        )

        self.assertContains(response, "Por favor ingrese un email valido")


    def test_should_response_with_404_status_if_provider_doesnt_exist(self):
        """"
        test para verificar que se muestre un error 404 si el proveedor no existe
        """
        response = self.client.get(reverse("providers_edit", kwargs={"id": 100}))
        self.assertEqual(response.status_code, 404)

    def test_can_delete_provider(self):
        """"
        test para verificar que se pueda eliminar un proveedor
        """
        provider = Provider.objects.create(
            name="Valentina", email="estudiantes@gmail.com", direccion="12 y 47",
        )
        response = self.client.post(reverse("providers_delete"), data={"provider_id": provider.id})
        self.assertEqual(response.status_code, 302)

        providers = Provider.objects.all()
        self.assertEqual(len(providers), 0)


    def test_edit_provider_with_valid_data(self):
        """"
        test para editar un proveedor con datos validos
        """
        provider = Provider.objects.create(
            name="Valentina", email="estudiantes@gmail.com", direccion="12 y 47",
        )

        response = self.client.post(
            reverse("providers_edit", kwargs={"id": provider.id}),
            data={
                "id": provider.id,
                "name": "Faustina",
                "email": "boca@gmail.com",
                "direccion": "12 y 50",
            },
        )
        self.assertEqual(response.status_code, 302)

        edited_provider = Provider.objects.get(pk=provider.id)
        self.assertEqual(edited_provider.name, "Faustina")
        self.assertEqual(edited_provider.email, "boca@gmail.com")
        self.assertEqual(edited_provider.direccion, "12 y 50")
