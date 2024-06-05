import os
from decimal import Decimal

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
from playwright.sync_api import Browser, expect, sync_playwright

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

os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
playwright = sync_playwright().start()
headless = True
slow_mo = os.environ.get("SLOW_MO", 0)


class PlaywrightTestCase(StaticLiveServerTestCase):
    """ Test base para Playwright """
    @classmethod
    def setUpClass(cls):
        """"
        Inicializa el navegador antes de ejecutar las pruebas
        """
        super().setUpClass()
        cls.browser: Browser = playwright.firefox.launch(
            headless=headless, slow_mo=int(slow_mo),
        )

    @classmethod
    def tearDownClass(cls):
        """"
        Cierra el navegador después de ejecutar las pruebas
        """
        super().tearDownClass()
        cls.browser.close()

    def setUp(self):
        """"
        Inicializa una nueva página antes de ejecutar cada prueba
        """
        super().setUp()
        self.page = self.browser.new_page()

    def tearDown(self):
        """"
        Cierra la página después de ejecutar cada prueba
        """
        super().tearDown()
        self.page.close()


class HomeTestCase(PlaywrightTestCase):
    """Caso de prueba para la página de inicio, este caso de prueba verificará que la página de inicio tenga los elementos y enlaces esperados."""
    def test_should_have_navbar_with_links(self):
        """"
        Verifica que el navbar tenga los links correctos
        """
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
        """"
        Verifica que las tarjetas de la página de inicio tengan los links correctos
        """
        self.page.goto(self.live_server_url)

        home_clients_link = self.page.get_by_test_id("home-Clientes")

        expect(home_clients_link).to_be_visible()
        expect(home_clients_link).to_have_text("Clientes")
        expect(home_clients_link).to_have_attribute("href", reverse("clients_repo"))


class ClientsRepoTestCase(PlaywrightTestCase):
    """Caso de prueba para el repositorio de clientes, este caso de prueba verificará que el repositorio de clientes tenga los elementos y enlaces esperados."""
    def test_should_show_message_if_table_is_empty(self):
        """"
        Verifica que se muestre un mensaje si la tabla está vacía
        """
        self.page.goto(f"{self.live_server_url}{reverse('clients_repo')}")

        expect(self.page.get_by_text("No existen clientes")).to_be_visible()

    def test_should_show_clients_data(self):
        """"
        Verifica que se muestren los datos de los clientes
        """
        Client.objects.create(
            name="Juan Sebastián Veron",
            city=CityEnum.LA_PLATA,
            phone="54221555232",
            email="brujita75@vetsoft.com",
        )

        Client.objects.create(
            name="Guido Carrillo",
            city=CityEnum.BERISSO,
            phone="54221232555",
            email="goleador@vetsoft.com",
        )

        self.page.goto(f"{self.live_server_url}{reverse('clients_repo')}")

        expect(self.page.get_by_text("No existen clientes")).not_to_be_visible()

        expect(self.page.get_by_text("Juan Sebastián Veron")).to_be_visible()
        expect(self.page.get_by_text("La Plata")).to_be_visible()
        expect(self.page.get_by_text("54221555232")).to_be_visible()
        expect(self.page.get_by_text("brujita75@vetsoft.com")).to_be_visible()

        expect(self.page.get_by_text("Guido Carrillo")).to_be_visible()
        expect(self.page.get_by_text("Berisso")).to_be_visible()
        expect(self.page.get_by_text("54221232555")).to_be_visible()
        expect(self.page.get_by_text("goleador@vetsoft.com")).to_be_visible()

    def test_should_show_add_client_action(self):
        """"
        Verifica que se muestre la acción de agregar cliente
        """
        self.page.goto(f"{self.live_server_url}{reverse('clients_repo')}")

        add_client_action = self.page.get_by_role(
            "link", name="Nuevo cliente", exact=False,
        )
        expect(add_client_action).to_have_attribute("href", reverse("clients_form"))

    def test_should_show_client_edit_action(self):
        """"
        Verifica que se muestre la acción de editar cliente"""
        client = Client.objects.create(
            name="Juan Sebastián Veron",
            city=CityEnum.LA_PLATA,
            phone="54221555232",
            email="brujita75@vetsoft.com",
        )

        self.page.goto(f"{self.live_server_url}{reverse('clients_repo')}")

        edit_action = self.page.get_by_role("link", name="Editar")
        expect(edit_action).to_have_attribute(
            "href", reverse("clients_edit", kwargs={"id": client.id}),
        )

    def test_should_show_client_delete_action(self):
        """"
        Verifica que se muestre la acción de eliminar cliente
        """
        client = Client.objects.create(
            name="Juan Sebastián Veron",
            city=CityEnum.LA_PLATA,
            phone="54221555232",
            email="brujita75@vetsoft.com",
        )

        self.page.goto(f"{self.live_server_url}{reverse('clients_repo')}")

        edit_form = self.page.get_by_role(
            "form", name="Formulario de eliminación de cliente",
        )
        client_id_input = edit_form.locator("input[name=client_id]")

        expect(edit_form).to_be_visible()
        expect(edit_form).to_have_attribute("action", reverse("clients_delete"))
        expect(client_id_input).not_to_be_visible()
        expect(client_id_input).to_have_value(str(client.id))
        expect(edit_form.get_by_role("button", name="Eliminar")).to_be_visible()

    def test_should_can_be_able_to_delete_a_client(self):
        """"
        Verifica que se pueda eliminar un cliente
        """
        Client.objects.create(
            name="Juan Sebastián Veron",
            city=CityEnum.LA_PLATA,
            phone="54221555232",
            email="brujita75@vetsoft.com",
        )

        self.page.goto(f"{self.live_server_url}{reverse('clients_repo')}")

        expect(self.page.get_by_text("Juan Sebastián Veron")).to_be_visible()
        expect(self.page.get_by_text("La Plata")).to_be_visible()
        expect(self.page.get_by_text("54221555232")).to_be_visible()
        expect(self.page.get_by_text("brujita75@vetsoft.com")).to_be_visible()


        def is_delete_response(response):
            return response.url.find(reverse("clients_delete"))

        # verificamos que el envio del formulario fue exitoso
        with self.page.expect_response(is_delete_response) as response_info:
            self.page.get_by_role("button", name="Eliminar").click()

        response = response_info.value
        self.assertTrue(response.status < 400)

        expect(self.page.get_by_text("Juan Sebastián Veron")).not_to_be_visible()
        expect(self.page.get_by_text("La Plata")).not_to_be_visible()
        expect(self.page.get_by_text("54221555232")).not_to_be_visible()
        expect(self.page.get_by_text("brujita75@vetsoft.com")).not_to_be_visible()


class ClientCreateEditTestCase(PlaywrightTestCase):
    """Caso de prueba para el formulario de clientes, este caso de prueba verificará que el formulario de clientes tenga los elementos y enlaces esperados."""
    def test_should_be_able_to_create_a_new_client(self):
        """"
        Verifica que se pueda crear un nuevo cliente
        """
        self.page.goto(f"{self.live_server_url}{reverse('clients_form')}")

        expect(self.page.get_by_role("form")).to_be_visible()

        self.page.get_by_label("Nombre").fill("Juan Sebastián Veron")
        self.page.get_by_label("Teléfono").fill("54221555232")
        self.page.get_by_label("Email").fill("brujita75@vetsoft.com")
        self.page.get_by_label("Ciudad").select_option("La Plata")

        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("Juan Sebastián Veron")).to_be_visible()
        expect(self.page.get_by_text("54221555232")).to_be_visible()
        expect(self.page.get_by_text("brujita75@vetsoft.com")).to_be_visible()
        expect(self.page.get_by_text("La Plata")).to_be_visible()

    def test_shouldnt_be_able_to_create_a_new_client_with_wrong_phone(self):
        """"
        Caso de prueba para el formulario de clientes, este caso de prueba verificará que no se crea un cliente con telefono incorrecto.
        """
        self.page.goto(f"{self.live_server_url}{reverse('clients_form')}")

        expect(self.page.get_by_role("form")).to_be_visible()

        self.page.get_by_label("Nombre").fill("Juan Sebastián Veron")
        self.page.get_by_label("Teléfono").fill("221555232")
        self.page.get_by_label("Email").fill("brujita75@vetsoft.com")
        self.page.get_by_label("Ciudad").select_option("La Plata")

        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("Por favor ingrese un teléfono válido")).to_be_visible()

    def test_shouldnt_be_able_to_create_a_new_client_with_empty_city(self):
        """"
        Caso de prueba para el formulario de clientes, este caso de prueba verificará que no se crea un cliente con ciudad incorrecta.
        """
        self.page.goto(f"{self.live_server_url}{reverse('clients_form')}")

        expect(self.page.get_by_role("form")).to_be_visible()

        self.page.get_by_label("Nombre").fill("Juan Sebastián Veron")
        self.page.get_by_label("Teléfono").fill("54221555232")
        self.page.get_by_label("Email").fill("brujita75@vetsoft.com")

        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("Por favor ingrese una ciudad")).to_be_visible()


    def test_should_view_errors_if_form_is_invalid(self):
        """"
        Verifica que se muestren errores si el formulario es inválido"""
        self.page.goto(f"{self.live_server_url}{reverse('clients_form')}")

        expect(self.page.get_by_role("form")).to_be_visible()

        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("Por favor ingrese un nombre")).to_be_visible()
        expect(self.page.get_by_text("Por favor ingrese un teléfono")).to_be_visible()
        expect(self.page.get_by_text("Por favor ingrese un email")).to_be_visible()
        expect(self.page.get_by_text("Por favor ingrese una ciudad")).to_be_visible()

        self.page.get_by_label("Nombre").fill("Juan Sebastián Veron")
        self.page.get_by_label("Teléfono").fill("54221555232")
        self.page.get_by_label("Email").fill("brujita75")
        self.page.get_by_label("Ciudad").select_option("La Plata")

        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("Por favor ingrese un nombre")).not_to_be_visible()
        expect(
            self.page.get_by_text("Por favor ingrese un teléfono"),
        ).not_to_be_visible()

        expect(
            self.page.get_by_text("Por favor ingrese un email valido"),
        ).to_be_visible()
        expect(self.page.get_by_text("Por favor ingrese una ciudad")).not_to_be_visible()

    def test_should_view_errors_if_phone_is_invalid(self):
        """"
        Verifica que se muestren errores si el formulario es inválido en caso de poner un telefono invalido"""
        self.page.goto(f"{self.live_server_url}{reverse('clients_form')}")

        expect(self.page.get_by_role("form")).to_be_visible()

        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("Por favor ingrese un nombre")).to_be_visible()
        expect(self.page.get_by_text("Por favor ingrese un teléfono")).to_be_visible()
        expect(self.page.get_by_text("Por favor ingrese un email")).to_be_visible()
        expect(self.page.get_by_text("Por favor ingrese una ciudad")).to_be_visible()


        self.page.get_by_label("Nombre").fill("Juan Sebastián Veron")
        self.page.get_by_label("Teléfono").fill("221555232")
        self.page.get_by_label("Email").fill("brujita75@vetsoft.com")
        self.page.get_by_label("Ciudad").select_option("La Plata")

        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("Por favor ingrese un nombre")).not_to_be_visible()
        expect(
            self.page.get_by_text("Por favor ingrese un teléfono válido"),
        ).to_be_visible()

        expect(
            self.page.get_by_text("Por favor ingrese un email valido"),
        ).not_to_be_visible()
        expect(self.page.get_by_text("Por favor ingrese una ciudad")).not_to_be_visible()

    def test_should_view_errors_if_phone_is_empty(self):
        """"
        Verifica que se muestren errores si el formulario es inválido en caso de poner un telefono invalido"""
        self.page.goto(f"{self.live_server_url}{reverse('clients_form')}")

        expect(self.page.get_by_role("form")).to_be_visible()

        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("Por favor ingrese un nombre")).to_be_visible()
        expect(self.page.get_by_text("Por favor ingrese un teléfono")).to_be_visible()
        expect(self.page.get_by_text("Por favor ingrese un email")).to_be_visible()
        expect(self.page.get_by_text("Por favor ingrese una ciudad")).to_be_visible()

        self.page.get_by_label("Nombre").fill("Juan Sebastián Veron")
        self.page.get_by_label("Teléfono").fill("")
        self.page.get_by_label("Email").fill("brujita75@vetsoft.com")
        self.page.get_by_label("Ciudad").select_option("La Plata")

        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("Por favor ingrese un nombre")).not_to_be_visible()
        expect(
            self.page.get_by_text("Por favor ingrese un teléfono"),
        ).to_be_visible()

        expect(
            self.page.get_by_text("Por favor ingrese un email valido"),
        ).not_to_be_visible()
        expect(self.page.get_by_text("Por favor ingrese una ciudad")).not_to_be_visible()


    def test_should_show_error_for_non_numeric_phone(self):
        """
        Verifica que se muestren errores si el teléfono no es numérico.
        """
        self.page.goto(f"{self.live_server_url}{reverse('clients_form')}")

        expect(self.page.get_by_role("form")).to_be_visible()

        self.page.get_by_label("Nombre").fill("Juan Sebastián Veron")
        self.page.get_by_label("Teléfono").fill("54 91134563456")
        ##Hago un test con un espacio adelante ya que es bastante comun que la gente lo ponga así,
        ##Otra manera de probarlo seria ponerle 54 11telefono o cualquier otra letra y también marcaría el error.
        self.page.get_by_label("Email").fill("brujita75@vetsoft.com")
        self.page.get_by_label("Ciudad").select_option("La Plata")
        self.page.get_by_role("button", name="Guardar").click()
        expect(self.page.get_by_text("Por favor ingrese solo valores numéricos")).to_be_visible()


    def test_should_view_errors_if_email_is_invalid(self):
        """"
        Verifica que se muestren errores si el formulario es inválido en caso de poner un email invalido"""
        self.page.goto(f"{self.live_server_url}{reverse('clients_form')}")

        expect(self.page.get_by_role("form")).to_be_visible()

        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("Por favor ingrese un nombre")).to_be_visible()
        expect(self.page.get_by_text("Por favor ingrese un teléfono")).to_be_visible()
        expect(self.page.get_by_text("Por favor ingrese un email")).to_be_visible()
        expect(self.page.get_by_text("Por favor ingrese una ciudad")).to_be_visible()

        self.page.get_by_label("Nombre").fill("Juan Sebastián Veron")
        self.page.get_by_label("Teléfono").fill("54221555232")
        self.page.get_by_label("Email").fill("brujita75@gmail.com")
        self.page.get_by_label("Ciudad").select_option("Ensenada")

        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("Por favor ingrese un nombre")).not_to_be_visible()
        expect(
            self.page.get_by_text("Por favor ingrese un teléfono válido"),
        ).not_to_be_visible()

        expect(
            self.page.get_by_text("El email debe terminar con @vetsoft.com"),
        ).to_be_visible()

    def test_should_view_errors_if_email_is_empty(self):
        """"
        Verifica que se muestren errores si el formulario es inválido en caso de poner un email vacio"""
        self.page.goto(f"{self.live_server_url}{reverse('clients_form')}")

        expect(self.page.get_by_role("form")).to_be_visible()

        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("Por favor ingrese un nombre")).to_be_visible()
        expect(self.page.get_by_text("Por favor ingrese un teléfono")).to_be_visible()
        expect(self.page.get_by_text("Por favor ingrese un email")).to_be_visible()
        expect(self.page.get_by_text("Por favor ingrese una ciudad")).to_be_visible()


        self.page.get_by_label("Nombre").fill("Juan Sebastián Veron")
        self.page.get_by_label("Teléfono").fill("54221555232")
        self.page.get_by_label("Email").fill("")
        self.page.get_by_label("Ciudad").select_option("Ensenada")

        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("Por favor ingrese un nombre")).not_to_be_visible()
        expect(
            self.page.get_by_text("Por favor ingrese un teléfono"),
        ).not_to_be_visible()

        expect(
            self.page.get_by_text("Por favor ingrese un email"),
        ).to_be_visible()
        expect(self.page.get_by_text("Por favor ingrese una ciudad")).not_to_be_visible()

    def test_shouldnt_be_able_to_create_a_new_client_with_wrong_email(self):
        """"
        Caso de prueba para el formulario de clientes, este caso de prueba verificará que no se crea un cliente con email incorrecto.
        """
        self.page.goto(f"{self.live_server_url}{reverse('clients_form')}")

        expect(self.page.get_by_role("form")).to_be_visible()

        self.page.get_by_label("Nombre").fill("Juan Sebastián Veron")
        self.page.get_by_label("Teléfono").fill("54221555232")
        self.page.get_by_label("Email").fill("brujita75@gmail.com")
        self.page.get_by_label("Ciudad").select_option("Ensenada")

        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("El email debe terminar con @vetsoft.com")).to_be_visible()

    def test_should_view_errors_if_name_is_invalid(self):
        """"
        Verifica que se muestren errores si el formulario es inválido en caso de poner un nombre invalido
        """
        self.page.goto(f"{self.live_server_url}{reverse('clients_form')}")

        expect(self.page.get_by_role("form")).to_be_visible()

        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("Por favor ingrese un nombre")).to_be_visible()
        expect(self.page.get_by_text("Por favor ingrese un teléfono")).to_be_visible()
        expect(self.page.get_by_text("Por favor ingrese un email")).to_be_visible()
        expect(self.page.get_by_text("Por favor ingrese una ciudad")).to_be_visible()


        self.page.get_by_label("Nombre").fill("Juan Sebastián 123")
        self.page.get_by_label("Teléfono").fill("54221555232")
        self.page.get_by_label("Email").fill("brujita75@vetsoft.com")
        self.page.get_by_label("Ciudad").select_option("La Plata")

        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("El nombre solo debe contener letras y espacios")).to_be_visible()
        expect(
            self.page.get_by_text("Por favor ingrese un teléfono válido"),
        ).not_to_be_visible()

        expect(
            self.page.get_by_text("Por favor ingrese un email valido"),
        ).not_to_be_visible()
        expect(self.page.get_by_text("Por favor ingrese una ciudad")).not_to_be_visible()

    def test_should_view_errors_if_name_is_empty(self):
        """"
        Verifica que se muestren errores si el formulario es inválido en caso de poner un nombre vacio
        """
        self.page.goto(f"{self.live_server_url}{reverse('clients_form')}")

        expect(self.page.get_by_role("form")).to_be_visible()

        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("Por favor ingrese un nombre")).to_be_visible()
        expect(self.page.get_by_text("Por favor ingrese un teléfono")).to_be_visible()
        expect(self.page.get_by_text("Por favor ingrese un email")).to_be_visible()
        expect(self.page.get_by_text("Por favor ingrese una ciudad")).to_be_visible()

        self.page.get_by_label("Nombre").fill("")
        self.page.get_by_label("Teléfono").fill("54221555232")
        self.page.get_by_label("Email").fill("brujita75@vetsoft.com")
        self.page.get_by_label("Ciudad").select_option("La Plata")

        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("Por favor ingrese un nombre")).to_be_visible()
        expect(
            self.page.get_by_text("Por favor ingrese un teléfono"),
        ).not_to_be_visible()

        expect(
            self.page.get_by_text("Por favor ingrese un email valido"),
        ).not_to_be_visible()
        expect(self.page.get_by_text("Por favor ingrese una ciudad")).not_to_be_visible()



    def test_should_be_able_to_edit_a_client(self):
        """"
        Verifica que se pueda editar un cliente
        """
        client = Client.objects.create(
            name="Juan Sebastián Veron",
            city=CityEnum.LA_PLATA,
            phone="54221555232",
            email="brujita75@vetsoft.com",
        )

        path = reverse("clients_edit", kwargs={"id": client.id})
        self.page.goto(f"{self.live_server_url}{path}")

        self.page.get_by_label("Nombre").fill("Guido Carrillo")
        self.page.get_by_label("Teléfono").fill("54221232555")
        self.page.get_by_label("Email").fill("goleador@vetsoft.com")
        self.page.get_by_label("Ciudad").select_option("Ensenada")

        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("Juan Sebastián Veron")).not_to_be_visible()
        expect(self.page.get_by_text("La Plata")).not_to_be_visible()
        expect(self.page.get_by_text("54221555232")).not_to_be_visible()
        expect(self.page.get_by_text("brujita75@vetsoft.com")).not_to_be_visible()

        expect(self.page.get_by_text("Guido Carrillo")).to_be_visible()
        expect(self.page.get_by_text("Ensenada")).to_be_visible()
        expect(self.page.get_by_text("54221232555")).to_be_visible()
        expect(self.page.get_by_text("goleador@vetsoft.com")).to_be_visible()

        edit_action = self.page.get_by_role("link", name="Editar")
        expect(edit_action).to_have_attribute(
            "href", reverse("clients_edit", kwargs={"id": client.id}),
        )


    def test_shouldnt_be_able_to_edit_a_client_with_invalid_phone(self):
        """"
        Verifica que no se pueda editar un cliente con telefono invalido
        """
        client = Client.objects.create(
            name="Juan Sebastián Veron",
            city=CityEnum.LA_PLATA,
            phone="54221555232",
            email="brujita75@vetsoft.com",
        )

        path = reverse("clients_edit", kwargs={"id": client.id})
        self.page.goto(f"{self.live_server_url}{path}")
        self.page.get_by_label("Nombre").fill("Guido Carrillo")
        self.page.get_by_label("Teléfono").fill("221232555")
        self.page.get_by_label("Email").fill("goleador@vetsoft.com")
        self.page.get_by_label("Ciudad").select_option("Berisso")
        self.page.get_by_role("button", name="Guardar").click()
        expect(self.page.get_by_text("Por favor ingrese un teléfono válido")).to_be_visible()

    def test_shouldnt_be_able_to_edit_a_client_with_empty_phone(self):
        """"
        Verifica que no se pueda editar un cliente con telefono vacio
        """
        client = Client.objects.create(
            name="Juan Sebastián Veron",
            city=CityEnum.LA_PLATA,
            phone="54221555232",
            email="brujita75@vetsoft.com",
        )

        path = reverse("clients_edit", kwargs={"id": client.id})
        self.page.goto(f"{self.live_server_url}{path}")
        self.page.get_by_label("Nombre").fill("Guido Carrillo")
        self.page.get_by_label("Teléfono").fill("")
        self.page.get_by_label("Email").fill("goleador@vetsoft.com")
        self.page.get_by_label("Ciudad").select_option("Berisso")
        self.page.get_by_role("button", name="Guardar").click()
        expect(self.page.get_by_text("Por favor ingrese un teléfono")).to_be_visible()


# validacion para pet


class PetsRepoTestCase(PlaywrightTestCase):
    """caso de prueba para el repositorio de mascotas, este caso de prueba verificará que el repositorio de mascotas tenga los elementos y enlaces esperados."""
    def test_should_show_message_if_table_is_empty(self):
        """"
        Verifica que se muestre un mensaje si la tabla está vacía
        """
        self.page.goto(f"{self.live_server_url}{reverse('pets_repo')}")

        expect(self.page.get_by_text("No existen Mascotas")).to_be_visible()

    def test_should_show_pets_data(self):
        """"
        Verifica que se muestren los datos de las mascotas
        """
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
        """"
        Verifica que se muestre la acción de agregar mascota
        """
        self.page.goto(f"{self.live_server_url}{reverse('pets_repo')}")

        add_client_action = self.page.get_by_role(
            "link", name="Nueva Mascota", exact=False,
        )
        expect(add_client_action).to_have_attribute("href", reverse("pets_form"))

    def test_should_show_pet_edit_action(self):
        """"
        Verifica que se muestre la acción de editar mascota
        """
        pet = Pet.objects.create(
            name="Juan Sebastián Veron",
            breed=Breed.PASTOR_ALEMAN,
            birthday="2024-05-13",
            weight= Decimal("70.50"),
        )

        self.page.goto(f"{self.live_server_url}{reverse('pets_repo')}")

        edit_action = self.page.get_by_role("link", name="Editar")
        expect(edit_action).to_have_attribute(
            "href", reverse("pets_edit", kwargs={"id": pet.id}),
        )

    def test_should_show_pet_delete_action(self):
        """"
        Verifica que se muestre la acción de eliminar mascota
        """
        pet = Pet.objects.create(
            name="Juan Sebastián Veron",
            breed=Breed.PASTOR_ALEMAN,
            birthday="2024-05-13",
            weight= Decimal("70.50"),
        )

        self.page.goto(f"{self.live_server_url}{reverse('pets_repo')}")

        edit_form = self.page.get_by_role(
            "form", name="Formulario de eliminación de Mascota",
        )
        pet_id_input = edit_form.locator("input[name=pet_id]")

        expect(edit_form).to_be_visible()
        expect(edit_form).to_have_attribute("action", reverse("pets_delete"))
        expect(pet_id_input).not_to_be_visible()
        expect(pet_id_input).to_have_value(str(pet.id))
        expect(edit_form.get_by_role("button", name="Eliminar")).to_be_visible()

    def test_should_can_be_able_to_delete_a_pet(self):
        """"
        Verifica que se pueda eliminar una mascota
        """
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
    """Caso de prueba para el formulario de mascotas, este caso de prueba verificará que el formulario de mascotas tenga los elementos y enlaces esperados."""
    def test_should_be_able_to_create_a_new_pet(self):
        """"
        Verifica que se pueda crear una nueva mascota
        """
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
        expect(self.page.get_by_text("10/")).to_be_visible()
        expect(self.page.get_by_text("70.50")).to_be_visible()

    def test_should_not_be_able_to_create_a_new_pet_invalidad_breed(self):
        """"
        Verifica que no se pueda crear una nueva mascota con raza inválida
        """
        self.page.goto(f"{self.live_server_url}{reverse('pets_form')}")

        expect(self.page.get_by_role("form")).to_be_visible()

        self.page.get_by_label("Nombre").fill("Juan Sebastián Veron")
        self.page.get_by_label("Raza").select_option("")
        self.page.get_by_label("Peso").fill("70.50")
        # Activar el calendario haciendo clic en el campo de fecha
        self.page.get_by_label("Fecha de Nacimiento").click()

        self.page.locator('text="10"').click()  # Ajusta este selector según la estructura exacta del calendario
        self.page.get_by_role("button", name="Guardar").click()
        expect(self.page.get_by_text("La raza es requerida.")).to_be_visible()


    def test_should_not_be_able_to_create_a_new_pet_invalidad_weight(self):
        """"
        Verifica que no se pueda crear una nueva mascota con peso inválido
        """
        self.page.goto(f"{self.live_server_url}{reverse('pets_form')}")

        expect(self.page.get_by_role("form")).to_be_visible()

        self.page.get_by_label("Nombre").fill("Juan Sebastián Veron")
        self.page.get_by_label("Raza").select_option("")
        self.page.get_by_label("Peso").fill("")
        # Activar el calendario haciendo clic en el campo de fecha
        self.page.get_by_label("Fecha de Nacimiento").click()

        self.page.locator('text="10"').click()  # Ajusta este selector según la estructura exacta del calendario
        self.page.get_by_role("button", name="Guardar").click()
        expect(self.page.get_by_text("El peso es requerido.")).to_be_visible()


    def test_should_view_errors_if_form_pet_is_empty_weight(self):
        """"
        Verifica que se muestren errores si el formulario de mascota está vacío
        """
        self.page.goto(f"{self.live_server_url}{reverse('pets_form')}")
        expect(self.page.get_by_role("form")).to_be_visible()
        self.page.get_by_role("button", name="Guardar").click()
        expect(self.page.get_by_text("El nombre es requerido.")).to_be_visible()
        expect(self.page.get_by_text("La raza es requerida.")).to_be_visible()
        expect(self.page.get_by_text("La fecha de nacimiento es requerida.")).to_be_visible()
        expect(self.page.get_by_text("El peso es requerido.")).to_be_visible()
        self.page.get_by_label("Nombre").fill("Juan Sebastián Veron")
        self.page.get_by_label("Fecha de Nacimiento").click()
        self.page.locator('text="10"').click()
        self.page.get_by_label("Raza").select_option("Golden Retriever")
        self.page.get_by_label("Peso").fill("")
        self.page.get_by_role("button", name="Guardar").click()
        expect(self.page.get_by_text("El nombre es requerido.")).not_to_be_visible()
        expect(self.page.get_by_text("La raza es requerida.")).not_to_be_visible()
        self.page.get_by_label("Fecha de Nacimiento").click()
        self.page.locator('text="10"').click()
        expect(self.page.get_by_text("La fecha de nacimiento es requerida.")).not_to_be_visible()
        expect(self.page.get_by_text("El peso es requerido.")).to_be_visible()

    def test_should_view_errors_if_form_pet_is_empty_breed(self):
        """"
        Verifica que se muestren errores si el formulario de mascota está vacío
        """
        self.page.goto(f"{self.live_server_url}{reverse('pets_form')}")
        expect(self.page.get_by_role("form")).to_be_visible()
        self.page.get_by_role("button", name="Guardar").click()
        expect(self.page.get_by_text("El nombre es requerido.")).to_be_visible()
        expect(self.page.get_by_text("La raza es requerida.")).to_be_visible()
        expect(self.page.get_by_text("La fecha de nacimiento es requerida.")).to_be_visible()
        expect(self.page.get_by_text("El peso es requerido.")).to_be_visible()
        self.page.get_by_label("Nombre").fill("Juan Sebastián Veron")
        self.page.get_by_label("Fecha de Nacimiento").click()
        self.page.locator('text="10"').click()
        self.page.get_by_label("Raza").select_option("")
        self.page.get_by_label("Peso").fill("33")
        self.page.get_by_role("button", name="Guardar").click()
        expect(self.page.get_by_text("El nombre es requerido.")).not_to_be_visible()
        expect(self.page.get_by_text("La raza es requerida.")).to_be_visible()
        self.page.get_by_label("Fecha de Nacimiento").click()
        self.page.locator('text="10"').click()
        expect(self.page.get_by_text("La fecha de nacimiento es requerida.")).not_to_be_visible()
        expect(self.page.get_by_text("El peso es requerido.")).not_to_be_visible()

    def test_should_be_able_to_edit_a_pet(self):
        """"
        Verifica que se pueda editar una mascota
        """
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
        self.page.locator('text="10"').click()
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
            "href", reverse("pets_edit", kwargs={"id": pet.id}),
        )

    def test_should_not_be_able_to_edit_a_pet_with_invalida_breed(self):
        """"
        Verifica que no se pueda editar una mascota con raza inválida
        """
        pet = Pet.objects.create(
            name="Juan Sebastián Veron",
            breed=Breed.PASTOR_ALEMAN,
            birthday="2024-05-13",
            weight= Decimal("70.50"),
        )

        path = reverse("pets_edit", kwargs={"id": pet.id})
        self.page.goto(f"{self.live_server_url}{path}")

        self.page.get_by_label("Nombre").fill("Guido Carrillo")
        self.page.get_by_label("Raza").select_option("")
        self.page.get_by_label("Fecha de Nacimiento").click()
        self.page.locator('text="10"').click()
        self.page.get_by_label("Peso").click()
        self.page.keyboard.press("ArrowUp")
        self.page.get_by_label("Peso").fill("10,00")

        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("La raza es requerida.")).to_be_visible()





class MedicineCreateEditTestCase(PlaywrightTestCase):
    """Caso de prueba para el formulario de medicamentos, este caso de prueba verificará que el formulario de medicamentos tenga los elementos y enlaces esperados."""
    def test_create_a_new_medicine_with_valid_dose(self):
        """"
        Creación con dosis válida
        """
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
        """"
        Error si la dosis está vacía
        """
        self.page.goto(f"{self.live_server_url}{reverse('medicines_form')}")

        expect(self.page.get_by_role("form")).to_be_visible()

        self.page.get_by_label("Nombre").fill("Aspirina")
        self.page.get_by_label("Descripcion").fill("Analgésico y antipirético")
        self.page.get_by_label("Dosis").fill("")

        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("Por favor ingrese una dosis")).to_be_visible()

    def test_error_if_dose_is_greater_than_10(self):
        """"
        Error si la dosis es mayor a 10
        """
        self.page.goto(f"{self.live_server_url}{reverse('medicines_form')}")

        expect(self.page.get_by_role("form")).to_be_visible()

        self.page.get_by_label("Nombre").fill("Aspirina")
        self.page.get_by_label("Descripcion").fill("Analgésico y antipirético")
        self.page.get_by_label("Dosis").fill("15")

        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("Por favor ingrese una dosis entre 1 y 10")).to_be_visible()

    def test_error_if_dose_is_less_than_1(self):
        """"
        Error si la dosis es menor a 1
        """
        self.page.goto(f"{self.live_server_url}{reverse('medicines_form')}")

        expect(self.page.get_by_role("form")).to_be_visible()

        self.page.get_by_label("Nombre").fill("Aspirina")
        self.page.get_by_label("Descripcion").fill("Analgésico y antipirético")
        self.page.get_by_label("Dosis").fill("-1")

        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("Por favor ingrese una dosis entre 1 y 10")).to_be_visible()



    def test_edit_medicine_with_valid_dose(self):
        """
        Edición con dosis válida
        """
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
        """"
        Edición sin ingresar dosis
        """
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
        """"
        Edición con dosis inválida
        """
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
        """"
        Edición con dosis inválida
        """
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


# TEST E2E PRODUCTO
class ProductsRepoTestCase(PlaywrightTestCase):
    """Caso de prueba para el repositorio de productos, este caso de prueba verificará que el repositorio de productos tenga los elementos y enlaces esperados."""
    def test_should_show_message_if_table_is_empty(self):
        """"
        Verifica que se muestre un mensaje si la tabla está vacía
        """
        self.page.goto(f"{self.live_server_url}{reverse('products_repo')}")

        expect(self.page.get_by_text("No existen productos")).to_be_visible()

    def test_should_show_products_data(self):
        """"
        Verifica que se muestren los datos de los productos
        """
        Product.objects.create(
            name="DogChow",
            type="Perro adulto",
            price="22145.45",
        )

        Product.objects.create(
            name="Whiskas",
            type="Gato adulto",
            price="20040.23",
        )

        self.page.goto(f"{self.live_server_url}{reverse('products_repo')}")

        expect(self.page.get_by_text("No existen productos")).not_to_be_visible()

        expect(self.page.get_by_text("DogChow")).to_be_visible()
        expect(self.page.get_by_text("Perro adulto")).to_be_visible()
        expect(self.page.get_by_text("22145.45")).to_be_visible()

        expect(self.page.get_by_text("Whiskas")).to_be_visible()
        expect(self.page.get_by_text("Gato adulto")).to_be_visible()
        expect(self.page.get_by_text("20040.23")).to_be_visible()

    def test_should_show_add_product_action(self):
        """"
        Verifica que se muestre la acción de agregar producto
        """
        self.page.goto(f"{self.live_server_url}{reverse('products_repo')}")

        add_product_action = self.page.get_by_role(
            "link", name="Nuevo producto", exact=False,
        )
        expect(add_product_action).to_have_attribute("href", reverse("products_form"))

    def test_should_show_product_edit_action(self):
        """"
        Verifica que se muestre la acción de editar producto
        """
        product = Product.objects.create(
            name="DogChow",
            type="Perro adulto",
            price="22145.45",
        )

        self.page.goto(f"{self.live_server_url}{reverse('products_repo')}")

        edit_action = self.page.get_by_role("link", name="Editar")
        expect(edit_action).to_have_attribute(
            "href", reverse("products_edit", kwargs={"id": product.id}),
        )

    def test_should_show_product_delete_action(self):
        """"
        Verifica que se muestre la acción de eliminar producto
        """
        product = Product.objects.create(
            name="DogChow",
            type="Perro adulto",
            price="22145.45",
        )

        self.page.goto(f"{self.live_server_url}{reverse('products_repo')}")

        edit_form = self.page.get_by_role(
            "form", name="Formulario de eliminación de producto",
        )
        product_id_input = edit_form.locator("input[name=product_id]")

        expect(edit_form).to_be_visible()
        expect(edit_form).to_have_attribute("action", reverse("products_delete"))
        expect(product_id_input).not_to_be_visible()
        expect(product_id_input).to_have_value(str(product.id))
        expect(edit_form.get_by_role("button", name="Eliminar")).to_be_visible()

    def test_should_can_be_able_to_delete_a_product(self):
        """"
        Verifica que se pueda eliminar un producto"""
        Product.objects.create(
            name="DogChow",
            type="Perro adulto",
            price="22145.45",
        )

        self.page.goto(f"{self.live_server_url}{reverse('products_repo')}")

        expect(self.page.get_by_text("DogChow")).to_be_visible()

        def is_delete_response(response):
            """"
            Verifica que se muestre la acción de eliminar producto
            """
            return response.url.find(reverse("products_delete"))

        # verificamos que el envio del formulario fue exitoso
        with self.page.expect_response(is_delete_response) as response_info:
            self.page.get_by_role("button", name="Eliminar").click()

        response = response_info.value
        self.assertTrue(response.status < 400)

        expect(self.page.get_by_text("DogChow")).not_to_be_visible()


class ProductCreateEditTestCase(PlaywrightTestCase):
    """Caso de prueba para el formulario de productos, este caso de prueba verificará que el formulario de productos tenga los elementos y enlaces esperados."""
    def test_should_be_able_to_create_a_new_product(self):
        """"
        Verifica que se pueda crear un nuevo producto
        """
        self.page.goto(f"{self.live_server_url}{reverse('products_form')}")

        expect(self.page.get_by_role("form")).to_be_visible()

        self.page.get_by_label("Nombre").fill("DogChow")
        self.page.get_by_label("Tipo").fill("Perro adulto")
        self.page.get_by_label("Precio").fill("22145.45")

        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("DogChow")).to_be_visible()
        expect(self.page.get_by_text("Perro adulto")).to_be_visible()
        expect(self.page.get_by_text("22145.45")).to_be_visible()

    def test_should_view_errors_if_form_is_invalid(self):
        """"
        Verifica que se muestren errores si el formulario es inválido
        """
        self.page.goto(f"{self.live_server_url}{reverse('products_form')}")

        expect(self.page.get_by_role("form")).to_be_visible()

        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("Por favor ingrese el nombre del producto")).to_be_visible()
        expect(self.page.get_by_text("Por favor ingrese el tipo de producto")).to_be_visible()
        expect(self.page.get_by_text("Por favor ingrese un precio válido")).to_be_visible()

        self.page.get_by_label("Nombre").fill("DogChow")
        self.page.get_by_label("Tipo").fill("Perro adulto")
        self.page.get_by_label("Precio").fill("0")

        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("Por favor ingrese el nombre del producto")).not_to_be_visible()
        expect(
            self.page.get_by_text("Por favor ingrese el tipo de producto"),
        ).not_to_be_visible()

        expect(
            self.page.get_by_text("Por favor ingrese un precio válido"),
        ).to_be_visible()

    def test_should_be_able_to_edit_a_product(self):
        """"
        Verifica que se pueda editar un producto
        """
        product = Product.objects.create(
            name="DogChow",
            type="Perro adulto",
            price="22145.45",
        )

        path = reverse("products_edit", kwargs={"id": product.id})
        self.page.goto(f"{self.live_server_url}{path}")

        self.page.get_by_label("Nombre").fill("Whiskas")
        self.page.get_by_label("Tipo").fill("Gato adulto")
        self.page.get_by_label("Precio").fill("20040.43")


        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("DogChow")).not_to_be_visible()
        expect(self.page.get_by_text("Perro adulto")).not_to_be_visible()
        expect(self.page.get_by_text("22145.45")).not_to_be_visible()

        expect(self.page.get_by_text("Whiskas")).to_be_visible()
        expect(self.page.get_by_text("Gato adulto")).to_be_visible()
        expect(self.page.get_by_text("20040.43")).to_be_visible()

        edit_action = self.page.get_by_role("link", name="Editar")
        expect(edit_action).to_have_attribute(
            "href", reverse("products_edit", kwargs={"id": product.id}),
        )

# #validacion para vet - speciality

class VetsRepoTestCase(PlaywrightTestCase):
    """Caso de prueba para el repositorio de veterinarios, este caso de prueba verificará que el repositorio de veterinarios tenga los elementos y enlaces esperados."""
    def test_should_show_message_if_table_is_empty(self):
        """"
        Verifica que se muestre un mensaje si la tabla está vacía
        """
        self.page.goto(f"{self.live_server_url}{reverse('vets_repo')}")

        expect(self.page.get_by_text("No existen veterinarios")).to_be_visible()

    def test_should_show_vets_data(self):
        """"
        Verifica que se muestren los datos de los veterinarios
        """
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

    def test_should_show_add_vet_action(self):
        """"
        Verifica que se muestre la acción de agregar veterinario
        """
        self.page.goto(f"{self.live_server_url}{reverse('vets_repo')}")

        add_client_action = self.page.get_by_role(
            "link", name="Nuevo Veterinario", exact=False,
        )
        expect(add_client_action).to_have_attribute("href", reverse("vets_form"))

    def test_should_show_vet_edit_action(self):
        """"
        Verifica que se muestre la acción de editar veterinario
        """
        vet = Vet.objects.create(
            name="Juan Sebastián Veron",
            email="brujita75@hotmail.com",
            phone="2215552324",
            speciality = Speciality.CARDIOLOGO,
        )

        self.page.goto(f"{self.live_server_url}{reverse('vets_repo')}")

        edit_action = self.page.get_by_role("link", name="Editar")
        expect(edit_action).to_have_attribute(
            "href", reverse("vets_edit", kwargs={"id": vet.id}),
        )

    def test_should_show_vet_delete_action(self):
        """"
        Verifica que se muestre la acción de eliminar veterinario
        """
        vet = Vet.objects.create(
            name="Juan Sebastián Veron",
            email="brujita75@hotmail.com",
            phone="2215552324",
            speciality = Speciality.CARDIOLOGO,
        )

        self.page.goto(f"{self.live_server_url}{reverse('vets_repo')}")

        edit_form = self.page.get_by_role(
            "form", name="Formulario de eliminación de veterinario",
        )
        vet_id_input = edit_form.locator("input[name=vet_id]")

        expect(edit_form).to_be_visible()
        expect(edit_form).to_have_attribute("action", reverse("vets_delete"))
        expect(vet_id_input).not_to_be_visible()
        expect(vet_id_input).to_have_value(str(vet.id))
        expect(edit_form.get_by_role("button", name="Eliminar")).to_be_visible()

    def test_should_can_be_able_to_delete_a_vet(self):
        """"
        Verifica que se pueda eliminar un veterinario
        """
        Vet.objects.create(
            name="Juan Sebastián Veron",
            email="brujita75@hotmail.com",
            phone="2215552324",
            speciality = Speciality.CARDIOLOGO,
        )

        self.page.goto(f"{self.live_server_url}{reverse('vets_repo')}")

        expect(self.page.get_by_text("Juan Sebastián Veron")).to_be_visible()

        def is_delete_response(response):
            """"
            Verifica que se muestre la acción de eliminar veterinario
            """
            return response.url.find(reverse("vets_delete"))

        # verificamos que el envio del formulario fue exitoso
        with self.page.expect_response(is_delete_response) as response_info:
            self.page.get_by_role("button", name="Eliminar").click()

        response = response_info.value
        self.assertTrue(response.status < 400)

        expect(self.page.get_by_text("Juan Sebastián Veron")).not_to_be_visible()


class VetCreateEditTestCase(PlaywrightTestCase):
    """Caso de prueba para el formulario de veterinarios, este caso de prueba verificará que el formulario de veterinarios tenga los elementos y enlaces esperados."""
    def test_should_be_able_to_create_a_new_vet(self):
        """"
        Verifica que se pueda crear un nuevo veterinario
        """
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
        """"
        Verifica que se muestren errores si el formulario de veterinario es inválido
        """
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
        """"
        Verifica que se pueda editar un veterinario
        """
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
            "href", reverse("vets_edit", kwargs={"id": vet.id}),
        )



#########################################


class ProvidersRepoTestCase(PlaywrightTestCase):
    """Caso de prueba para el repositorio de proveedores, este caso de prueba verificará que el repositorio de proveedores tenga los elementos y enlaces esperados."""
    def test_should_show_message_if_table_is_empty(self):
        """"
        Verifica que se muestre un mensaje si la tabla está vacía
        """
        self.page.goto(f"{self.live_server_url}{reverse('providers_repo')}")

        expect(self.page.get_by_text("No existen Proveedores")).to_be_visible()

    def test_should_show_providers_data(self):
        """"
        Verifica que se muestren los datos de los proveedores
        """
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
        """"
        Verifica que se muestre la acción de agregar proveedor
        """
        self.page.goto(f"{self.live_server_url}{reverse('providers_repo')}")

        add_client_action = self.page.get_by_role(
            "link", name="Nuevo Proveedor", exact=False,
        )
        expect(add_client_action).to_have_attribute("href", reverse("providers_form"))

    def test_should_show_provider_edit_action(self):
        """"
        Verifica que se muestre la acción de editar proveedor
        """
        provider = Provider.objects.create(
            name="Juan Sebastián Veron",
            email="brujita75@hotmail.com",
            direccion="mi casa",
        )

        self.page.goto(f"{self.live_server_url}{reverse('providers_repo')}")

        edit_action = self.page.get_by_role("link", name="Editar")
        expect(edit_action).to_have_attribute(
            "href", reverse("providers_edit", kwargs={"id": provider.id}),
        )

    def test_should_show_provider_delete_action(self):
        """"
        Verifica que se muestre la acción de eliminar proveedor
        """
        provider = Provider.objects.create(
            name="Juan Sebastián Veron",
            email="brujita75@hotmail.com",
            direccion="mi casa",
        )

        self.page.goto(f"{self.live_server_url}{reverse('providers_repo')}")

        edit_form = self.page.get_by_role(
            "form", name="Formulario de eliminación de proveedor",
        )
        provider_id_input = edit_form.locator("input[name=provider_id]")

        expect(edit_form).to_be_visible()
        expect(edit_form).to_have_attribute("action", reverse("providers_delete"))
        expect(provider_id_input).not_to_be_visible()
        expect(provider_id_input).to_have_value(str(provider.id))
        expect(edit_form.get_by_role("button", name="Eliminar")).to_be_visible()

    def test_should_can_be_able_to_delete_a_provider(self):
        """"
        Verifica que se pueda eliminar un proveedor
        """
        Provider.objects.create(
            name="Juan Sebastián Veron",
            email="brujita75@hotmail.com",
            direccion="mi casa",
        )

        self.page.goto(f"{self.live_server_url}{reverse('providers_repo')}")

        expect(self.page.get_by_text("Juan Sebastián Veron")).to_be_visible()

        def is_delete_response(response):
            """"
            Verifica que se muestre la acción de eliminar proveedor
            """
            return response.url.find(reverse("providers_delete"))

        # verificamos que el envio del formulario fue exitoso
        with self.page.expect_response(is_delete_response) as response_info:
            self.page.get_by_role("button", name="Eliminar").click()

        response = response_info.value
        self.assertTrue(response.status < 400)

        expect(self.page.get_by_text("Juan Sebastián Veron")).not_to_be_visible()


class ProviderCreateEditTestCase(PlaywrightTestCase):
    """Caso de prueba para el formulario de proveedores, este caso de prueba verificará que el formulario de proveedores tenga los elementos y enlaces esperados."""
    def test_should_be_able_to_create_a_new_provider(self):
        """"
        Creación de un proveedor
        """
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
        """"
        Verifica que se muestren errores si el formulario de proveedor es inválido
        """
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

        """"
        Edición de un proveedor
        """
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
            "href", reverse("providers_edit", kwargs={"id": provider.id}),
        )



