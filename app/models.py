from django.db import models
from datetime import datetime
import re

def validate_client(data):
    errors = {}

    name = data.get("name", "")
    phone = data.get("phone", "")
    email = data.get("email", "")

    if name == "":
        errors["name"] = "Por favor ingrese un nombre"

    if phone == "":
        errors["phone"] = "Por favor ingrese un teléfono"

    if email == "":
        errors["email"] = "Por favor ingrese un email"
    elif email.count("@") == 0:
        errors["email"] = "Por favor ingrese un email valido"

    return errors


class Client(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    address = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name

    @classmethod
    def save_client(cls, client_data):
        errors = validate_client(client_data)

        if len(errors.keys()) > 0:
            return False, errors

        Client.objects.create(
            name=client_data.get("name"),
            phone=client_data.get("phone"),
            email=client_data.get("email"),
            address=client_data.get("address"),
        )

        return True, None

    def update_client(self, client_data):
        self.name = client_data.get("name", "") or self.name
        self.email = client_data.get("email", "") or self.email
        self.phone = client_data.get("phone", "") or self.phone
        self.address = client_data.get("address", "") or self.address

        self.save()



def validate_vet(data):
    errors = {}

    name = data.get("name", "")
    phone = data.get("phone", "")
    email = data.get("email", "")

    if name == "":
        errors["name"] = "Por favor ingrese un nombre"

    if phone == "":
        errors["phone"] = "Por favor ingrese un teléfono"

    if email == "":
        errors["email"] = "Por favor ingrese un email"
    elif email.count("@") == 0:
        errors["email"] = "Por favor ingrese un email valido"

    return errors



class Vet(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)

    def __str__(self):
        return self.name

    @classmethod
    def save_vet(cls, vet_data):
        errors = validate_vet(vet_data)

        if len(errors.keys()) > 0:
            return False, errors

        Vet.objects.create(
            name=vet_data.get("name"),
            phone=vet_data.get("phone"),
            email=vet_data.get("email"),
        )

        return True, None

    def update_vet(self, vet_data):
        self.name = vet_data.get("name", "") or self.name
        self.email = vet_data.get("email", "") or self.email
        self.phone = vet_data.get("phone", "") or self.phone

        self.save()


def validate_provider(data):
    errors = {}

    name = data.get("name", "")
    email = data.get("email", "")

    if name == "":
        errors["name"] = "Por favor ingrese un nombre"

    if email == "":
        errors["email"] = "Por favor ingrese un email"
    elif email.count("@") == 0:
        errors["email"] = "Por favor ingrese un email valido"

    return errors


class Provider(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()

    def __str__(self):
        return self.name

    @classmethod
    def save_provider(cls, provider_data):
        errors = validate_provider(provider_data)

        if len(errors.keys()) > 0:
            return False, errors

        Provider.objects.create(
            name=provider_data.get("name"),
            email=provider_data.get("email"),
        )

        return True, None

    def update_provider(self, provider_data):
        self.name = provider_data.get("name", "") or self.name
        self.email = provider_data.get("email", "") or self.email
        self.save()

#Pet model
def validate_pet(pet_data):
    errors = {}
    if not pet_data.get("name"):
        errors["name"] = "El nombre es requerido."
    if not pet_data.get("breed"):
        errors["breed"] = "La raza es requerida."
    if not pet_data.get("birthday"):
        errors["birthday"] = "La fecha de nacimiento es requerida."
    if not parse_date(pet_data.get("birthday")):
        errors["birthday"] = "Formato de fecha incorrecto. Debe ser DD/MM/YYYY."

    return errors

def parse_date(date_str):
    try:
        return datetime.strptime(date_str, "%d/%m/%Y").date()
    except ValueError:
        return None  # Retorna None si hay un error en la conversión, con none se puede validar si la fecha es correcta o no

class Pet(models.Model):
    name = models.CharField(max_length=100)
    breed = models.CharField(max_length=100)
    birthday = models.DateField()

    def __str__(self):
        return self.name

    @classmethod
    def save_pet(cls, pet_data):
        errors = validate_pet(pet_data)
        if errors:
            return False, errors

        Pet.objects.create(
            name=pet_data.get("name"),
            breed=pet_data.get("breed"),
            birthday=parse_date(pet_data.get("birthday")),
        )

        return True, None

    def update_pet(self, pet_data):
        errors = validate_pet(pet_data)
        if errors:
            return False, errors

        self.name = pet_data.get("name", self.name)
        self.breed = pet_data.get("breed", self.breed)
        self.birthday = parse_date(pet_data.get("birthday")) or self.birthday

        self.save()
        return True, None



class Medicine(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=300)
    dose = models.IntegerField()

    def __str__(self):
        return self.name

    @classmethod
    def save_medicine(cls, medicine_data):
        errors = validate_medicine(medicine_data)

        if len(errors.keys()) > 0:
            return False, errors

        Medicine.objects.create(
            name=medicine_data.get("name"),
            description=medicine_data.get("description"),
            dose=medicine_data.get("dose"),
        )

        return True, None

    def update_medicine(self, medicine_data):
        self.name = medicine_data.get("name", "") or self.name
        self.description = medicine_data.get("description", "") or self.description
        self.dose = medicine_data.get("dose", "") or self.dose

        self.save()

def validate_medicine(data):
    errors = {}

    name = data.get("name", "")
    description = data.get("description", "")
    dose = data.get("dose", "")

    if name == "":
        errors["name"] = "Por favor ingrese un nombre"

    if description == "":
        errors["description"] = "Por favor ingrese una descripción"

    if dose == "":
        errors["dose"] = "Por favor ingrese una dosis"

    if dose != "":
        try:
            int(dose)
            if int(dose) < 0:
                errors["dose"] = "Por favor ingrese una dosis válida"
        except ValueError:
            errors["dose"] = "Por favor ingrese una dosis válida"


    return errors


def validate_product(data):
    errors = {}

    name = data.get("name", "")
    type = data.get("type", "")
    price_str = data.get("price", "")

    if name == "":
        errors["name"] = "Por favor ingrese el nombre del producto"

    if type == "":
        errors["type"] = "Por favor ingrese el tipo de producto"

    try:
        price = float(price_str)
        if price < 0:
            errors["price"] = "Por favor ingrese un precio positivo"
        if not validate_price_format(price_str):
            errors["price"] = "El precio debe tener un formato correcto (n.nn)"
    except ValueError:
        errors["price"] = "Por favor ingrese un precio válido"

    return errors

def validate_price_format(price_str):
    pattern = r"^\d+(\.\d+)?$"
    match = re.match(pattern, price_str)
    return match is not None


class Product(models.Model):
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=50)
    price = models.FloatField(max_length=20)

    def __str__(self):
        return self.name

    @classmethod
    def save_product(cls, product_data):
        errors = validate_product(product_data)

        if len(errors.keys()) > 0:
            return False, errors

        Product.objects.create(
            name=product_data.get("name"),
            type=product_data.get("type"),
            price=product_data.get("price"),
        )

        return True, None

    def update_product(self, product_data):
        self.name = product_data.get("name", "") or self.name
        self.type = product_data.get("type", "") or self.type
        self.price = product_data.get("price", "") or self.price

        self.save()
