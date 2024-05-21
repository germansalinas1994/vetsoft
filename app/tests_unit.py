from django.test import TestCase
from app.models import Client
from app.models import Medicine


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

    

   