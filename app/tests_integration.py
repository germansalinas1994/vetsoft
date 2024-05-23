from django.test import TestCase
from django.shortcuts import reverse
from app.models import Client
from app.models import Medicine



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

           

