from django.test import TestCase
from django.shortcuts import reverse
from app.models import Client
from app.models import Medicine
from app.models import Pet
from app.models import Vet, Speciality
from decimal import Decimal
from datetime import datetime


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


class MedicinesTest(TestCase):
    def test_repo_use_repo_template(self):
        response = self.client.get(reverse("medicines_repo"))
        self.assertTemplateUsed(response, "medicines/repository.html")

    def test_repo_display_all_medicines(self):
        Medicine.objects.create(name="Ivermectina", description="ectoparásitos y endoparásitos", dose=5)
        Medicine.objects.create(name="Frontline ", description="pulgas y piojos", dose=3)

        response = self.client.get(reverse("medicines_repo"))
        self.assertTemplateUsed(response, "medicines/repository.html")
        self.assertContains(response, "Ivermectina")
        self.assertContains(response, "Frontline ")

    def test_form_use_form_template(self):
        response = self.client.get(reverse("medicines_form"))
        self.assertTemplateUsed(response, "medicines/form.html")

    def test_can_create_medicine(self):
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
        response = self.client.post(reverse("medicines_form"), data={})
        self.assertContains(response, "Por favor ingrese un nombre")
        self.assertContains(response, "Por favor ingrese una descripción")
        self.assertContains(response, "Por favor ingrese una dosis")

    def test_validation_invalid_dose_is_greater_than_10(self):
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
        response = self.client.get(reverse("medicines_edit", kwargs={"id": 100}))
        self.assertEqual(response.status_code, 404)

    def test_can_delete_medicine(self):
        medicine = Medicine.objects.create(
            name="Ivermectina", description="ectoparásitos y endoparásitos", dose=5
        )
        response = self.client.post(reverse("medicines_delete"), data={"medicine_id": medicine.id})
        self.assertEqual(response.status_code, 302)

        medicines = Medicine.objects.all()
        self.assertEqual(len(medicines), 0)


    def test_edit_medicine_with_valid_data(self):
        medicine = Medicine.objects.create(
            name="Ivermectina", description="ectoparásitos y endoparásitos", dose=5
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
    # defino el test de la pagina de inicio para mascota y el template que se va a usar
    # esto es para chequear que la pagina de inicio de mascotas use el template correcto
    def test_repo_use_repo_template(self):
        response = self.client.get(reverse("pets_repo"))
        self.assertTemplateUsed(response, "pets/repository.html")

    # defino el test para ver si se muestran todas las mascotas en la pagina de inicio
    def test_repo_display_all_pets(self):
        response = self.client.get(reverse("pets_repo"))
        self.assertTemplateUsed(response, "pets/repository.html")

    # defino el test para ver si se usa el template correcto en el formulario de mascotas
    def test_form_use_form_template(self):
        response = self.client.get(reverse("pets_form"))
        self.assertTemplateUsed(response, "pets/form.html")


    # defino el test para crear una mascota
    def test_can_create_pet(self):
        response = self.client.post(
            reverse("pets_form"),
            data={
                "name": "Fido",
                "breed": "Golden Retriever",
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
        response = self.client.get(reverse("pets_edit", kwargs={"id": 100}))
        self.assertEqual(response.status_code, 404)

    # creo un test para verificar si el peso de la mascota es invalido
    def test_validation_invalid_weight(self):
        response = self.client.post(
            reverse("pets_form"),
            data={
                "name": "Fido",
                "breed": "Golden Retriever",
                "birthday": "01/01/2015",
                "weight": "invalid",
            },
        )
        # verifico que se muestre el error de validacion
        self.assertContains(response, "El peso debe ser un número positivo con hasta dos decimales.")

    def test_validation_errors_create_pet(self):
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
        # Creación de una mascota con datos iniciales.
        pet = Pet.objects.create(
            name="Fido",
            breed="Golden Retriever",
            birthday="2015-01-01",
            weight="10.50",
        )

        # Intento de editar la mascota enviando datos en el formato correcto.
        response = self.client.post(
            reverse("pets_edit", kwargs={"id": pet.id}),
            data ={
                "id": pet.id,
                "name": "cambio",
                "breed": "cambio",
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
    def test_repo_use_repo_template_vet(self):
        response = self.client.get(reverse("vets_repo"))
        self.assertTemplateUsed(response, "vets/repository.html")

    def test_repo_display_all_vets(self):
        response = self.client.get(reverse("vets_repo"))
        self.assertTemplateUsed(response, "vets/repository.html")

    def test_form_use_form_template_vet(self):
        response = self.client.get(reverse("vets_form"))
        self.assertTemplateUsed(response, "vets/form.html")

    def test_can_create_vet(self):
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
        response = self.client.post(
            reverse("vets_form"),
            data={},
        )

        self.assertContains(response, "Por favor ingrese un nombre")
        self.assertContains(response, "Por favor ingrese un teléfono")
        self.assertContains(response, "Por favor ingrese un email")
        self.assertContains(response, "Por favor ingrese una especialidad")

    def test_should_response_with_404_status_if_vet_doesnt_exists(self):
        response = self.client.get(reverse("vets_edit", kwargs={"id": 1000}))
        self.assertEqual(response.status_code, 404)

    def test_validation_invalid_speciality(self):
        response = self.client.post(
            reverse("vets_form"),
            data={
                "name": "Juan Sebastian Veron",
                "email": "brujita75@hotmail.com",
                "phone": "2215552324",
                "speciality": "esta especialidad no existe",
            },
        )


    def test_validation_invalid_speciality_none(self):
        response = self.client.post(
            reverse("vets_form"),
            data={
                "name": "Juan Sebastian Veron",
                "email": "brujita75@hotmail.com",
                "phone": "2215552324",
            },
        )

    def test_validation_invalid_speciality_empty(self):
        response = self.client.post(
            reverse("vets_form"),
            data={
                "name": "Juan Sebastian Veron",
                "email": "brujita75@hotmail.com",
                "phone": "",
            },
        )

    def test_edit_vet_with_valid_data(self):
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
