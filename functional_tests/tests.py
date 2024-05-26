import os

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from playwright.sync_api import sync_playwright, expect, Browser

from django.urls import reverse
from app.models import Provider
from app.models import Client
from app.models import Medicine
from app.models import Pet
from app.models import Vet, Speciality, Breed
from decimal import Decimal

os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
playwright = sync_playwright().start()
headless = True
slow_mo = os.environ.get("SLOW_MO", 0)


class PlaywrightTestCase(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.browser: Browser = playwright.firefox.launch(
            headless=headless, slow_mo=int(slow_mo)
        )

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cls.browser.close()

    def setUp(self):
        super().setUp()
        self.page = self.browser.new_page()

    def tearDown(self):
        super().tearDown()
        self.page.close()


class HomeTestCase(PlaywrightTestCase):
    def test_should_have_navbar_with_links(self):
        self.page.goto(self.live_server_url)

        navbar_home_link = self.page.get_by_test_id("navbar-Home")

        expect(navbar_home_link).to_be_visible()
        expect(navbar_home_link).to_have_text("Home")
        expect(navbar_home_link).to_have_attribute("href", reverse("home"))

        navbar_clients_link = self.page.get_by_test_id("navbar-Clientes")

        expect(navbar_clients_link).to_be_visible()
        expect(navbar_clients_link).to_have_text("Clientes")
        expect(navbar_clients_link).to_have_attribute("href", reverse("clients_repo"))

    def test_should_have_home_cards_with_links(self):
        self.page.goto(self.live_server_url)

        home_clients_link = self.page.get_by_test_id("home-Clientes")

        expect(home_clients_link).to_be_visible()
        expect(home_clients_link).to_have_text("Clientes")
        expect(home_clients_link).to_have_attribute("href", reverse("clients_repo"))


class ClientsRepoTestCase(PlaywrightTestCase):
    def test_should_show_message_if_table_is_empty(self):
        self.page.goto(f"{self.live_server_url}{reverse('clients_repo')}")

        expect(self.page.get_by_text("No existen clientes")).to_be_visible()

    def test_should_show_clients_data(self):
        Client.objects.create(
            name="Juan Sebastián Veron",
            address="13 y 44",
            phone="221555232",
            email="brujita75@hotmail.com",
        )

        Client.objects.create(
            name="Guido Carrillo",
            address="1 y 57",
            phone="221232555",
            email="goleador@gmail.com",
        )

        self.page.goto(f"{self.live_server_url}{reverse('clients_repo')}")

        expect(self.page.get_by_text("No existen clientes")).not_to_be_visible()

        expect(self.page.get_by_text("Juan Sebastián Veron")).to_be_visible()
        expect(self.page.get_by_text("13 y 44")).to_be_visible()
        expect(self.page.get_by_text("221555232")).to_be_visible()
        expect(self.page.get_by_text("brujita75@hotmail.com")).to_be_visible()

        expect(self.page.get_by_text("Guido Carrillo")).to_be_visible()
        expect(self.page.get_by_text("1 y 57")).to_be_visible()
        expect(self.page.get_by_text("221232555")).to_be_visible()
        expect(self.page.get_by_text("goleador@gmail.com")).to_be_visible()

    def test_should_show_add_client_action(self):
        self.page.goto(f"{self.live_server_url}{reverse('clients_repo')}")

        add_client_action = self.page.get_by_role(
            "link", name="Nuevo cliente", exact=False
        )
        expect(add_client_action).to_have_attribute("href", reverse("clients_form"))

    def test_should_show_client_edit_action(self):
        client = Client.objects.create(
            name="Juan Sebastián Veron",
            address="13 y 44",
            phone="221555232",
            email="brujita75@hotmail.com",
        )

        self.page.goto(f"{self.live_server_url}{reverse('clients_repo')}")

        edit_action = self.page.get_by_role("link", name="Editar")
        expect(edit_action).to_have_attribute(
            "href", reverse("clients_edit", kwargs={"id": client.id})
        )

    def test_should_show_client_delete_action(self):
        client = Client.objects.create(
            name="Juan Sebastián Veron",
            address="13 y 44",
            phone="221555232",
            email="brujita75@hotmail.com",
        )

        self.page.goto(f"{self.live_server_url}{reverse('clients_repo')}")

        edit_form = self.page.get_by_role(
            "form", name="Formulario de eliminación de cliente"
        )
        client_id_input = edit_form.locator("input[name=client_id]")

        expect(edit_form).to_be_visible()
        expect(edit_form).to_have_attribute("action", reverse("clients_delete"))
        expect(client_id_input).not_to_be_visible()
        expect(client_id_input).to_have_value(str(client.id))
        expect(edit_form.get_by_role("button", name="Eliminar")).to_be_visible()

    def test_should_can_be_able_to_delete_a_client(self):
        Client.objects.create(
            name="Juan Sebastián Veron",
            address="13 y 44",
            phone="221555232",
            email="brujita75@hotmail.com",
        )

        self.page.goto(f"{self.live_server_url}{reverse('clients_repo')}")

        expect(self.page.get_by_text("Juan Sebastián Veron")).to_be_visible()

        def is_delete_response(response):
            return response.url.find(reverse("clients_delete"))

        # verificamos que el envio del formulario fue exitoso
        with self.page.expect_response(is_delete_response) as response_info:
            self.page.get_by_role("button", name="Eliminar").click()

        response = response_info.value
        self.assertTrue(response.status < 400)

        expect(self.page.get_by_text("Juan Sebastián Veron")).not_to_be_visible()


class ClientCreateEditTestCase(PlaywrightTestCase):
    def test_should_be_able_to_create_a_new_client(self):
        self.page.goto(f"{self.live_server_url}{reverse('clients_form')}")

        expect(self.page.get_by_role("form")).to_be_visible()

        self.page.get_by_label("Nombre").fill("Juan Sebastián Veron")
        self.page.get_by_label("Teléfono").fill("221555232")
        self.page.get_by_label("Email").fill("brujita75@hotmail.com")
        self.page.get_by_label("Dirección").fill("13 y 44")

        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("Juan Sebastián Veron")).to_be_visible()
        expect(self.page.get_by_text("221555232")).to_be_visible()
        expect(self.page.get_by_text("brujita75@hotmail.com")).to_be_visible()
        expect(self.page.get_by_text("13 y 44")).to_be_visible()

    def test_should_view_errors_if_form_is_invalid(self):
        self.page.goto(f"{self.live_server_url}{reverse('clients_form')}")

        expect(self.page.get_by_role("form")).to_be_visible()

        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("Por favor ingrese un nombre")).to_be_visible()
        expect(self.page.get_by_text("Por favor ingrese un teléfono")).to_be_visible()
        expect(self.page.get_by_text("Por favor ingrese un email")).to_be_visible()

        self.page.get_by_label("Nombre").fill("Juan Sebastián Veron")
        self.page.get_by_label("Teléfono").fill("221555232")
        self.page.get_by_label("Email").fill("brujita75")
        self.page.get_by_label("Dirección").fill("13 y 44")

        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("Por favor ingrese un nombre")).not_to_be_visible()
        expect(
            self.page.get_by_text("Por favor ingrese un teléfono")
        ).not_to_be_visible()

        expect(
            self.page.get_by_text("Por favor ingrese un email valido")
        ).to_be_visible()

    def test_should_be_able_to_edit_a_client(self):
        client = Client.objects.create(
            name="Juan Sebastián Veron",
            address="13 y 44",
            phone="221555232",
            email="brujita75@hotmail.com",
        )

        path = reverse("clients_edit", kwargs={"id": client.id})
        self.page.goto(f"{self.live_server_url}{path}")

        self.page.get_by_label("Nombre").fill("Guido Carrillo")
        self.page.get_by_label("Teléfono").fill("221232555")
        self.page.get_by_label("Email").fill("goleador@gmail.com")
        self.page.get_by_label("Dirección").fill("1 y 57")

        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("Juan Sebastián Veron")).not_to_be_visible()
        expect(self.page.get_by_text("13 y 44")).not_to_be_visible()
        expect(self.page.get_by_text("221555232")).not_to_be_visible()
        expect(self.page.get_by_text("brujita75@hotmail.com")).not_to_be_visible()

        expect(self.page.get_by_text("Guido Carrillo")).to_be_visible()
        expect(self.page.get_by_text("1 y 57")).to_be_visible()
        expect(self.page.get_by_text("221232555")).to_be_visible()
        expect(self.page.get_by_text("goleador@gmail.com")).to_be_visible()

        edit_action = self.page.get_by_role("link", name="Editar")
        expect(edit_action).to_have_attribute(
            "href", reverse("clients_edit", kwargs={"id": client.id})
        )




#validacion para pet


class PetsRepoTestCase(PlaywrightTestCase):
    def test_should_show_message_if_table_is_empty(self):
        self.page.goto(f"{self.live_server_url}{reverse('pets_repo')}")

        expect(self.page.get_by_text("No existen Mascotas")).to_be_visible()

    def test_should_show_pets_data(self):
        Pet.objects.create(
            name="Juan Sebastián Veron",
            breed=Breed.PASTOR_ALEMAN,
            birthday="2024-05-13",
            weight= Decimal("70.50"),
        )

        Pet.objects.create(
            name="Guido Carrillo",
            breed=Breed.BEAGLE,
            birthday="2024-05-10",
            weight= Decimal("100.50"),
        )

        self.page.goto(f"{self.live_server_url}{reverse('pets_repo')}")

        expect(self.page.get_by_text("No existen Mascotas")).not_to_be_visible()

        expect(self.page.get_by_text("Juan Sebastián Veron")).to_be_visible()
        expect(self.page.get_by_text("Pastor Alemán")).to_be_visible()
        expect(self.page.get_by_text("13/05/2024")).to_be_visible()
        expect(self.page.get_by_text("70.50")).to_be_visible()

        expect(self.page.get_by_text("Guido Carrillo")).to_be_visible()
        expect(self.page.get_by_text("Beagle")).to_be_visible()
        expect(self.page.get_by_text("10/05/2024")).to_be_visible()
        expect(self.page.get_by_text("100.50")).to_be_visible()

    def test_should_show_add_pet_action(self):
        self.page.goto(f"{self.live_server_url}{reverse('pets_repo')}")

        add_client_action = self.page.get_by_role(
            "link", name="Nueva Mascota", exact=False
        )
        expect(add_client_action).to_have_attribute("href", reverse("pets_form"))

    def test_should_show_pet_edit_action(self):
        pet = Pet.objects.create(
            name="Juan Sebastián Veron",
            breed=Breed.PASTOR_ALEMAN,
            birthday="2024-05-13",
            weight= Decimal("70.50"),
        )

        self.page.goto(f"{self.live_server_url}{reverse('pets_repo')}")

        edit_action = self.page.get_by_role("link", name="Editar")
        expect(edit_action).to_have_attribute(
            "href", reverse("pets_edit", kwargs={"id": pet.id})
        )

    def test_should_show_pet_delete_action(self):
        pet = Pet.objects.create(
            name="Juan Sebastián Veron",
            breed=Breed.PASTOR_ALEMAN,
            birthday="2024-05-13",
            weight= Decimal("70.50"),
        )

        self.page.goto(f"{self.live_server_url}{reverse('pets_repo')}")

        edit_form = self.page.get_by_role(
            "form", name="Formulario de eliminación de Mascota"
        )
        pet_id_input = edit_form.locator("input[name=pet_id]")

        expect(edit_form).to_be_visible()
        expect(edit_form).to_have_attribute("action", reverse("pets_delete"))
        expect(pet_id_input).not_to_be_visible()
        expect(pet_id_input).to_have_value(str(pet.id))
        expect(edit_form.get_by_role("button", name="Eliminar")).to_be_visible()

    def test_should_can_be_able_to_delete_a_pet(self):
        Pet.objects.create(
            name="Juan Sebastián Veron",
            breed=Breed.PASTOR_ALEMAN,
            birthday="2024-05-13",
            weight= Decimal("70.50"),
        )

        self.page.goto(f"{self.live_server_url}{reverse('pets_repo')}")

        expect(self.page.get_by_text("Juan Sebastián Veron")).to_be_visible()

        def is_delete_response(response):
            return response.url.find(reverse("pets_delete"))

        # verificamos que el envio del formulario fue exitoso
        with self.page.expect_response(is_delete_response) as response_info:
            self.page.get_by_role("button", name="Eliminar").click()

        response = response_info.value
        self.assertTrue(response.status < 400)

        expect(self.page.get_by_text("Juan Sebastián Veron")).not_to_be_visible()



class PetCreateEditTestCase(PlaywrightTestCase):
    def test_should_be_able_to_create_a_new_pet(self):
        self.page.goto(f"{self.live_server_url}{reverse('pets_form')}")

        expect(self.page.get_by_role("form")).to_be_visible()

        self.page.get_by_label("Nombre").fill("Juan Sebastián Veron")
        self.page.get_by_label("Raza").select_option("Golden Retriever")
        self.page.get_by_label("Peso").fill("70.50")
        # Activar el calendario haciendo clic en el campo de fecha
        self.page.get_by_label("Fecha de Nacimiento").click()

        self.page.locator('text="10"').click()  # Ajusta este selector según la estructura exacta del calendario
        self.page.get_by_role("button", name="Guardar").click()
        expect(self.page.get_by_text("Juan Sebastián Veron")).to_be_visible()
        expect(self.page.get_by_text("Golden Retriever")).to_be_visible()
        expect(self.page.get_by_text("10/05/2024")).to_be_visible()
        expect(self.page.get_by_text("70.50")).to_be_visible()

    def test_should_view_errors_if_form_pet_is_invalid(self):
        self.page.goto(f"{self.live_server_url}{reverse('pets_form')}")

        expect(self.page.get_by_role("form")).to_be_visible()

        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("El nombre es requerido.")).to_be_visible()
        expect(self.page.get_by_text("La raza es requerida.")).to_be_visible()
        expect(self.page.get_by_text("La fecha de nacimiento es requerida.")).to_be_visible()
        expect(self.page.get_by_text("El peso es requerido.")).to_be_visible()

        self.page.get_by_label("Nombre").fill("Juan Sebastián Veron")
        self.page.get_by_label("Fecha de Nacimiento").click()
        self.page.locator('text="10"').click()  # Ajusta este selector según la estructura exacta del calendario
        self.page.get_by_label("Peso").fill("")

        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("El nombre es requerido.")).not_to_be_visible()
        expect(
            self.page.get_by_text("La raza es requerida.")
        ).to_be_visible()
        self.page.get_by_label("Fecha de Nacimiento").click()
        self.page.locator('text="10"').click()  # Ajusta este selector según la estructura exacta del calendario
        expect(self.page.get_by_text("La fecha de nacimiento es requerida.")).not_to_be_visible()
        expect(
            self.page.get_by_text("El peso es requerido.")
        ).to_be_visible()

    def test_should_be_able_to_edit_a_pet(self):
        pet = Pet.objects.create(
            name="Juan Sebastián Veron",
            breed=Breed.PASTOR_ALEMAN,
            birthday="2024-05-13",
            weight= Decimal("70.50"),
        )

        path = reverse("pets_edit", kwargs={"id": pet.id})
        self.page.goto(f"{self.live_server_url}{path}")

        self.page.get_by_label("Nombre").fill("Guido Carrillo")
        self.page.get_by_label("Raza").select_option("Golden Retriever")
        self.page.get_by_label("Fecha de Nacimiento").click()
        self.page.locator('text="10"').click()  # Ajusta este selector según la estructura exacta del calendario
        self.page.get_by_label("Peso").click()
        self.page.keyboard.press("ArrowUp")
        self.page.get_by_label("Peso").fill("10,00")

        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("Juan Sebastián Veron")).not_to_be_visible()
        expect(self.page.get_by_text("Pastor Alemán")).not_to_be_visible()
        expect(self.page.get_by_text("13/05/2024")).not_to_be_visible()
        expect(self.page.get_by_text("70.50")).not_to_be_visible()

        expect(self.page.get_by_text("Guido Carrillo")).to_be_visible()
        expect(self.page.get_by_text("Golden Retriever")).to_be_visible()
        expect(self.page.get_by_text("10/05/2024")).to_be_visible()
        expect(self.page.get_by_text("1000")).to_be_visible()

        edit_action = self.page.get_by_role("link", name="Editar")
        expect(edit_action).to_have_attribute(
            "href", reverse("pets_edit", kwargs={"id": pet.id})
        )


class MedicineCreateEditTestCase(PlaywrightTestCase):
    def test_create_a_new_medicine_with_valid_dose(self):
        self.page.goto(f"{self.live_server_url}{reverse('medicines_form')}")

        expect(self.page.get_by_role("form")).to_be_visible()

        self.page.get_by_label("Nombre").fill("Aspirina")
        self.page.get_by_label("Descripcion").fill("Analgésico y antipirético")
        self.page.get_by_label("Dosis").fill("5")

        self.page.get_by_role("button", name="Guardar").click()

        expected_url = f"{self.live_server_url}{reverse('medicines_repo')}"
        expect(self.page).to_have_url(expected_url)
        expect(self.page.get_by_text("Aspirina")).to_be_visible()
        expect(self.page.get_by_text("Analgésico y antipirético")).to_be_visible()
        expect(self.page.get_by_text("5")).to_be_visible()


    def test_error_if_dose_is_empty(self):
        self.page.goto(f"{self.live_server_url}{reverse('medicines_form')}")

        expect(self.page.get_by_role("form")).to_be_visible()

        self.page.get_by_label("Nombre").fill("Aspirina")
        self.page.get_by_label("Descripcion").fill("Analgésico y antipirético")
        self.page.get_by_label("Dosis").fill("")

        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("Por favor ingrese una dosis")).to_be_visible()

    def test_error_if_dose_is_greater_than_10(self):
        self.page.goto(f"{self.live_server_url}{reverse('medicines_form')}")

        expect(self.page.get_by_role("form")).to_be_visible()

        self.page.get_by_label("Nombre").fill("Aspirina")
        self.page.get_by_label("Descripcion").fill("Analgésico y antipirético")
        self.page.get_by_label("Dosis").fill("15")

        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("Por favor ingrese una dosis entre 1 y 10")).to_be_visible()

    def test_error_if_dose_is_less_than_1(self):
        self.page.goto(f"{self.live_server_url}{reverse('medicines_form')}")

        expect(self.page.get_by_role("form")).to_be_visible()

        self.page.get_by_label("Nombre").fill("Aspirina")
        self.page.get_by_label("Descripcion").fill("Analgésico y antipirético")
        self.page.get_by_label("Dosis").fill("-1")

        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("Por favor ingrese una dosis entre 1 y 10")).to_be_visible()



    def test_edit_medicine_with_valid_dose(self):
    # Edición con dosis válida
        medicine = Medicine.objects.create(
            name="Aspirina",
            description="Analgésico y antipirético",
            dose=5,
        )

        path = reverse("medicines_edit", kwargs={"id": medicine.id})
        self.page.goto(f"{self.live_server_url}{path}")

        self.page.get_by_label("Nombre").fill("Paracetamol")
        self.page.get_by_label("Descripcion").fill("Analgésico y antipirético")
        self.page.get_by_label("Dosis").fill("8")

        self.page.get_by_role("button", name="Guardar").click()

        expected_url = f"{self.live_server_url}{reverse('medicines_repo')}"
        expect(self.page).to_have_url(expected_url)
        expect(self.page.get_by_text("Paracetamol")).to_be_visible()
        expect(self.page.get_by_text("8")).to_be_visible()


    def test_edit_medicine_without_dose(self):
        # Edición sin ingresar dosis
        medicine = Medicine.objects.create(
            name="Aspirina",
            description="Analgésico y antipirético",
            dose=5,
        )

        path = reverse("medicines_edit", kwargs={"id": medicine.id})
        self.page.goto(f"{self.live_server_url}{path}")

        self.page.get_by_label("Dosis").fill("")
        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("Por favor ingrese una dosis")).to_be_visible()

    def test_edit_medicine_with_dose_is_less_than_1(self):
        # Edición con dosis inválida
        medicine = Medicine.objects.create(
            name="Aspirina",
            description="Analgésico y antipirético",
            dose=5,
        )

        path = reverse("medicines_edit", kwargs={"id": medicine.id})
        self.page.goto(f"{self.live_server_url}{path}")

        self.page.get_by_label("Dosis").fill("-12")
        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("Por favor ingrese una dosis entre 1 y 10")).to_be_visible()

    def test_edit_medicine_with_dose_is_greater_than_10(self):
        # Edición con dosis inválida
        medicine = Medicine.objects.create(
            name="Aspirina",
            description="Analgésico y antipirético",
            dose=5,
        )

        path = reverse("medicines_edit", kwargs={"id": medicine.id})
        self.page.goto(f"{self.live_server_url}{path}")

        self.page.get_by_label("Dosis").fill("15")
        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("Por favor ingrese una dosis entre 1 y 10")).to_be_visible()


# #validacion para vet - speciality

class VetsRepoTestCase(PlaywrightTestCase):
    def test_should_show_message_if_table_is_empty(self):
        self.page.goto(f"{self.live_server_url}{reverse('vets_repo')}")

        expect(self.page.get_by_text("No existen veterinarios")).to_be_visible()

    def test_should_show_vets_data(self):
        Vet.objects.create(
            name="Juan Sebastián Veron",
            email="brujita75@hotmail.com",
            phone="2214202799",
            speciality = Speciality.CARDIOLOGO,
        )

        Vet.objects.create(
            name="Guido Carrillo",
            email="guidito@hotmail.com",
            phone="2214202798",
            speciality = Speciality.GENERAL,
        )

        self.page.goto(f"{self.live_server_url}{reverse('vets_repo')}")

        expect(self.page.get_by_text("No existen veterinarios")).not_to_be_visible()

        expect(self.page.get_by_text("Juan Sebastián Veron")).to_be_visible()
        expect(self.page.get_by_text("brujita75@hotmail.com")).to_be_visible()
        expect(self.page.get_by_text("221-420-2799")).to_be_visible()
        expect(self.page.get_by_text("Cardiología")).to_be_visible()

        expect(self.page.get_by_text("Guido Carrillo")).to_be_visible()
        expect(self.page.get_by_text("guidito@hotmail.com")).to_be_visible()
        expect(self.page.get_by_text("221-420-2798")).to_be_visible()
        expect(self.page.get_by_text("General")).to_be_visible()

    def test_should_show_add_client_action(self):
        self.page.goto(f"{self.live_server_url}{reverse('vets_repo')}")

        add_client_action = self.page.get_by_role(
            "link", name="Nuevo Veterinario", exact=False
        )
        expect(add_client_action).to_have_attribute("href", reverse("vets_form"))

    def test_should_show_vet_edit_action(self):
        vet = Vet.objects.create(
            name="Juan Sebastián Veron",
            email="brujita75@hotmail.com",
            phone="2215552324",
            speciality = Speciality.CARDIOLOGO,
        )

        self.page.goto(f"{self.live_server_url}{reverse('vets_repo')}")

        edit_action = self.page.get_by_role("link", name="Editar")
        expect(edit_action).to_have_attribute(
            "href", reverse("vets_edit", kwargs={"id": vet.id})
        )

    def test_should_show_vet_delete_action(self):
        vet = Vet.objects.create(
            name="Juan Sebastián Veron",
            email="brujita75@hotmail.com",
            phone="2215552324",
            speciality = Speciality.CARDIOLOGO,
        )

        self.page.goto(f"{self.live_server_url}{reverse('vets_repo')}")

        edit_form = self.page.get_by_role(
            "form", name="Formulario de eliminación de veterinario"
        )
        vet_id_input = edit_form.locator("input[name=vet_id]")

        expect(edit_form).to_be_visible()
        expect(edit_form).to_have_attribute("action", reverse("vets_delete"))
        expect(vet_id_input).not_to_be_visible()
        expect(vet_id_input).to_have_value(str(vet.id))
        expect(edit_form.get_by_role("button", name="Eliminar")).to_be_visible()

    def test_should_can_be_able_to_delete_a_vet(self):
        Vet.objects.create(
            name="Juan Sebastián Veron",
            email="brujita75@hotmail.com",
            phone="2215552324",
            speciality = Speciality.CARDIOLOGO,
        )

        self.page.goto(f"{self.live_server_url}{reverse('vets_repo')}")

        expect(self.page.get_by_text("Juan Sebastián Veron")).to_be_visible()

        def is_delete_response(response):
            return response.url.find(reverse("vets_delete"))

        # verificamos que el envio del formulario fue exitoso
        with self.page.expect_response(is_delete_response) as response_info:
            self.page.get_by_role("button", name="Eliminar").click()

        response = response_info.value
        self.assertTrue(response.status < 400)

        expect(self.page.get_by_text("Juan Sebastián Veron")).not_to_be_visible()


class VetCreateEditTestCase(PlaywrightTestCase):
    def test_should_be_able_to_create_a_new_vet(self):
        self.page.goto(f"{self.live_server_url}{reverse('vets_form')}")

        expect(self.page.get_by_role("form")).to_be_visible()

        self.page.get_by_label("Nombre").fill("Juan Sebastián Veron")
        self.page.get_by_label("Teléfono").fill("2214202798")
        self.page.get_by_label("Email").fill("brujita75@hotmail.com")
        self.page.get_by_label("Especialidad").select_option("Cardiologo")

        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("Juan Sebastián Veron")).to_be_visible()
        expect(self.page.get_by_text("221-420-2798")).to_be_visible()
        expect(self.page.get_by_text("brujita75@hotmail.com")).to_be_visible()
        expect(self.page.get_by_text("Cardiología")).to_be_visible()

    def test_should_view_errors_if_form_vet_is_invalid(self):
        self.page.goto(f"{self.live_server_url}{reverse('vets_form')}")

        expect(self.page.get_by_role("form")).to_be_visible()

        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("Por favor ingrese un nombre")).to_be_visible()
        expect(self.page.get_by_text("Por favor ingrese un teléfono")).to_be_visible()
        expect(self.page.get_by_text("Por favor ingrese un email")).to_be_visible()
        expect(self.page.get_by_text("Por favor ingrese una especialidad")).to_be_visible()

        self.page.get_by_label("Nombre").fill("Juan Sebastián Veron")
        self.page.get_by_label("Teléfono").fill("2214202798")
        self.page.get_by_label("Email").fill("brujita75")
        self.page.get_by_label("Especialidad").select_option("Cardiologo")

        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("Por favor ingrese un nombre")).not_to_be_visible()
        expect(self.page.get_by_text("Por favor ingrese un teléfono")).not_to_be_visible()
        expect(self.page.get_by_text("Por favor ingrese una especialidad")).not_to_be_visible()
        expect(self.page.get_by_text("Por favor ingrese un email valido")).to_be_visible()

    def test_should_be_able_to_edit_a_vet(self):
        vet = Vet.objects.create(
            name="Juan Sebastián Veron",
            email="brujita75@hotmail.com",
            phone="2215552324",
            speciality = Speciality.CARDIOLOGO,
        )

        path = reverse("vets_edit", kwargs={"id": vet.id})
        self.page.goto(f"{self.live_server_url}{path}")

        self.page.get_by_label("Nombre").fill("Guido Carrillo")
        self.page.get_by_label("Teléfono").fill("2215019642")
        self.page.get_by_label("Email").fill("carrillito@gmail.com")
        self.page.get_by_label("Especialidad").select_option("General")

        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("Juan Sebastián Veron")).not_to_be_visible()
        expect(self.page.get_by_text("brujita75@hotmail.com")).not_to_be_visible()
        expect(self.page.get_by_text("2215552324")).not_to_be_visible()
        expect(self.page.get_by_text("Cardiología")).not_to_be_visible()

        expect(self.page.get_by_text("Guido Carrillo")).to_be_visible()
        expect(self.page.get_by_text("221-501-9642")).to_be_visible()
        expect(self.page.get_by_text("carrillito@gmail.com")).to_be_visible()
        expect(self.page.get_by_text("General")).to_be_visible()

        edit_action = self.page.get_by_role("link", name="Editar")
        expect(edit_action).to_have_attribute(
            "href", reverse("vets_edit", kwargs={"id": vet.id})
        )



#########################################


class ProvidersRepoTestCase(PlaywrightTestCase):
    def test_should_show_message_if_table_is_empty(self):
        self.page.goto(f"{self.live_server_url}{reverse('providers_repo')}")

        expect(self.page.get_by_text("No existen Proveedores")).to_be_visible()

    def test_should_show_providers_data(self):
        Provider.objects.create(
            name="Juan Sebastián Veron",
            email="brujita75@hotmail.com",
            direccion="mi casa",
        )

        Provider.objects.create(
            name="Guido Carrillo",
            email="guidito@hotmail.com",
            direccion="la facu",
        )

        self.page.goto(f"{self.live_server_url}{reverse('providers_repo')}")

        expect(self.page.get_by_text("No existen proveedores")).not_to_be_visible()

        expect(self.page.get_by_text("Juan Sebastián Veron")).to_be_visible()
        expect(self.page.get_by_text("brujita75@hotmail.com")).to_be_visible()
        expect(self.page.get_by_text("mi casa")).to_be_visible()

        expect(self.page.get_by_text("Guido Carrillo")).to_be_visible()
        expect(self.page.get_by_text("guidito@hotmail.com")).to_be_visible()
        expect(self.page.get_by_text("la facu")).to_be_visible()

    def test_should_show_add_client_action(self):
        self.page.goto(f"{self.live_server_url}{reverse('providers_repo')}")

        add_client_action = self.page.get_by_role(
            "link", name="Nuevo Proveedor", exact=False
        )
        expect(add_client_action).to_have_attribute("href", reverse("providers_form"))

    def test_should_show_provider_edit_action(self):
        provider = Provider.objects.create(
            name="Juan Sebastián Veron",
            email="brujita75@hotmail.com",
            direccion="mi casa",
        )

        self.page.goto(f"{self.live_server_url}{reverse('providers_repo')}")

        edit_action = self.page.get_by_role("link", name="Editar")
        expect(edit_action).to_have_attribute(
            "href", reverse("providers_edit", kwargs={"id": provider.id})
        )

    def test_should_show_provider_delete_action(self):
        provider = Provider.objects.create(
            name="Juan Sebastián Veron",
            email="brujita75@hotmail.com",
            direccion="mi casa",
        )

        self.page.goto(f"{self.live_server_url}{reverse('providers_repo')}")

        edit_form = self.page.get_by_role(
            "form", name="Formulario de eliminación de proveedor"
        )
        provider_id_input = edit_form.locator("input[name=provider_id]")

        expect(edit_form).to_be_visible()
        expect(edit_form).to_have_attribute("action", reverse("providers_delete"))
        expect(provider_id_input).not_to_be_visible()
        expect(provider_id_input).to_have_value(str(provider.id))
        expect(edit_form.get_by_role("button", name="Eliminar")).to_be_visible()

    def test_should_can_be_able_to_delete_a_provider(self):
        Provider.objects.create(
            name="Juan Sebastián Veron",
            email="brujita75@hotmail.com",
            direccion="mi casa",
        )

        self.page.goto(f"{self.live_server_url}{reverse('providers_repo')}")

        expect(self.page.get_by_text("Juan Sebastián Veron")).to_be_visible()

        def is_delete_response(response):
            return response.url.find(reverse("providers_delete"))

        # verificamos que el envio del formulario fue exitoso
        with self.page.expect_response(is_delete_response) as response_info:
            self.page.get_by_role("button", name="Eliminar").click()

        response = response_info.value
        self.assertTrue(response.status < 400)

        expect(self.page.get_by_text("Juan Sebastián Veron")).not_to_be_visible()


class ProviderCreateEditTestCase(PlaywrightTestCase):
    def test_should_be_able_to_create_a_new_provider(self):
        self.page.goto(f"{self.live_server_url}{reverse('providers_form')}")

        expect(self.page.get_by_role("form")).to_be_visible()

        self.page.get_by_label("Nombre").fill("Juan Sebastián Veron")
        self.page.get_by_label("Email").fill("brujita75@hotmail.com")
        self.page.get_by_label("Direccion").fill("mi casa")

        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("Juan Sebastián Veron")).to_be_visible()
        expect(self.page.get_by_text("brujita75@hotmail.com")).to_be_visible()
        expect(self.page.get_by_text("mi casa")).to_be_visible()

    def test_should_view_errors_if_form_provider_is_invalid(self):
        self.page.goto(f"{self.live_server_url}{reverse('providers_form')}")

        expect(self.page.get_by_role("form")).to_be_visible()

        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("Por favor ingrese un nombre")).to_be_visible()
        expect(self.page.get_by_text("Por favor ingrese un email")).to_be_visible()
        expect(self.page.get_by_text("Por favor ingrese una direccion")).to_be_visible()

        self.page.get_by_label("Nombre").fill("Juan Sebastián Veron")
        self.page.get_by_label("Email").fill("brujita75")
        self.page.get_by_label("Direccion").fill("mi casa")

        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("Por favor ingrese un nombre")).not_to_be_visible()
        expect(self.page.get_by_text("Por favor ingrese un email valido")).to_be_visible()
        expect(self.page.get_by_text("Por favor ingrese una direccion")).not_to_be_visible()

    def test_should_be_able_to_edit_a_provider(self):
        provider = Provider.objects.create(
            name="Juan Sebastián Veron",
            email="brujita75@hotmail.com",
            direccion= "mi casa",
        )

        path = reverse("providers_edit", kwargs={"id": provider.id})
        self.page.goto(f"{self.live_server_url}{path}")

        self.page.get_by_label("Nombre").fill("Guido Carrillo")
        self.page.get_by_label("Email").fill("carrillito@gmail.com")
        self.page.get_by_label("Direccion").fill("la facu")

        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("Juan Sebastián Veron")).not_to_be_visible()
        expect(self.page.get_by_text("brujita75@hotmail.com")).not_to_be_visible()
        expect(self.page.get_by_text("mi casa")).not_to_be_visible()

        expect(self.page.get_by_text("Guido Carrillo")).to_be_visible()
        expect(self.page.get_by_text("carrillito@gmail.com")).to_be_visible()
        expect(self.page.get_by_text("la facu")).to_be_visible()

        edit_action = self.page.get_by_role("link", name="Editar")
        expect(edit_action).to_have_attribute(
            "href", reverse("providers_edit", kwargs={"id": provider.id})
        )



