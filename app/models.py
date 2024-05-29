from django.db import models
from datetime import datetime
import re
from decimal import Decimal


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




class Speciality(models.TextChoices):
    GENERAL = "General"
    DENTISTA = "Dentista"
    TRAUMATOLOGO = "Traumatología"
    DERMATOLOGO = "Dermatología"
    CARDIOLOGO = "Cardiología"



class Vet(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    speciality = models.CharField(max_length=50, choices=Speciality.choices, default=Speciality.GENERAL)

    def __str__(self):
        return self.name

    def get_speciality_display(self):
        return self.get_speciality_display()
    def formatted_phone(self):
        return f"{self.phone[:3]}-{self.phone[3:6]}-{self.phone[6:]}"

    @classmethod
    def save_vet(cls, vet_data):
        errors = validate_vet(vet_data)

        if len(errors.keys()) > 0:
            return False, errors

        Vet.objects.create(
            name=vet_data.get("name"),
            phone=vet_data.get("phone"),
            email=vet_data.get("email"),
            speciality=vet_data.get("speciality"),
        )

        return True, None

    def update_vet(self, vet_data):
        errors = validate_vet(vet_data)
        if len(errors.keys()) > 0:
            return False, errors

        self.name = vet_data.get("name", "") or self.name
        self.email = vet_data.get("email", "") or self.email
        self.phone = vet_data.get("phone", "") or self.phone
        self.speciality = vet_data.get("speciality", "") or self.speciality
        self.save()

        return True, None

def validate_vet(data):
    errors = {}

    name = data.get("name", "")
    phone = data.get("phone", "")
    email = data.get("email", "")
    speciality = data.get("speciality", "")

    if name == "" or name == None:
        errors["name"] = "Por favor ingrese un nombre"


    if phone == "" or phone == None:
        errors["phone"] = "Por favor ingrese un teléfono"
    else:
        error = validate_phone(phone)
        if error != None:
            errors["phone"] = validate_phone(phone)


    if email == "" or email == None:
        errors["email"] = "Por favor ingrese un email"
    elif email.count("@") == 0:
        errors["email"] = "Por favor ingrese un email valido"

    if speciality == "" or speciality == None:
        errors["speciality"] = "Por favor ingrese una especialidad"
    elif speciality not in dict(Speciality.choices):
        errors["speciality"] = "Especialidad no válida"

    return errors

def validate_phone(phone):
    #le extraigo los guiones al teléfono y guion bajo
    phone = phone.replace("-", "").replace("_", "")
    if len(phone) == 10:
        #verifico que el teléfono tenga solo numeros
        try:
            int(phone)
        except ValueError:
            return "Por favor ingrese un teléfono válido"
    else:
        return "Por favor ingrese un teléfono válido"

    return None

def validate_provider(data):
    errors = {}

    name = data.get("name", "")
    email = data.get("email", "")
    direccion = data.get("direccion", "")

    if name == "":
        errors["name"] = "Por favor ingrese un nombre"

    if email == "":
        errors["email"] = "Por favor ingrese un email"
    elif email.count("@") == 0:
        errors["email"] = "Por favor ingrese un email valido"

    if direccion == "":
       errors["direccion"] = "Por favor ingrese una direccion"

    return errors



class Provider(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    direccion = models.CharField(max_length=100, blank=True)

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
            direccion=provider_data.get("direccion")
        )

        return True, None

    def update_provider(self, provider_data):
        errors = validate_provider(provider_data)
        if len(errors.keys()) > 0:
            return False, errors

        self.name = provider_data.get("name", "") or self.name
        self.email = provider_data.get("email", "") or self.email
        self.direccion = provider_data.get("direccion", "") or self.direccion
        self.save()
        return True, None


# Pet model

def validate_pet(pet_data):
    errors = {}
    # valido que el nombre no este vacio ni sea null
    name = pet_data.get("name")

    if not name or name == None:
        errors["name"] = "El nombre es requerido."
    if name == "":
        errors["name"] = "El nombre es requerido."
    # valido que la raza no este vacia ni sea null
    breed = pet_data.get("breed","")

    if breed == "" or breed == None:
        errors["breed"] = "La raza es requerida."
    elif breed not in dict(Breed.choices):
        errors["breed"] = "La raza no es válida."

    # valido que la fecha de nacimiento no este vacia ni sea null
    birthday = pet_data.get("birthday")

    if not birthday or birthday == None:
        errors["birthday"] = "La fecha de nacimiento es requerida."
    elif not parse_date(birthday):
        errors["birthday"] = "Formato de fecha incorrecto. Debe ser DD/MM/YYYY."
    if birthday == "":
        errors["birthday"] = "La fecha de nacimiento es requerida."
    # valido que el peso no este vacio ni sea null
    weight = pet_data.get("weight")

    if not weight or weight == None:
        errors["weight"] = "El peso es requerido."
    else:
        weight_error = validate_weight(weight)
        if weight_error:
            errors["weight"] = weight_error
    return errors


def validate_weight(weight):
    try:
        weight_value = float(weight)
    except (ValueError, TypeError):
        return "El peso debe ser un número positivo con hasta dos decimales."

    if weight_value < 0:
        return "El peso no debe ser menor que 0."
    if round(weight_value, 2) != weight_value:
        return "El peso debe tener hasta dos decimales."

    return None


def parse_date(date_str):
    try:
        if not date_str:
            return None
        return datetime.strptime(date_str, "%d/%m/%Y").date()
    except ValueError:
        return None  # Retorna None si hay un error en la conversión, con none se puede validar si la fecha es correcta o no


class Breed(models.TextChoices):
        LABRADOR_RETRIEVER = 'Labrador Retriever'
        PASTOR_ALEMAN = 'Pastor Alemán'
        GOLDEN_RETRIEVER = 'Golden Retriever'
        BEAGLE = 'Beagle'
        BOXER = 'Boxer'
        SIAMES = 'Siamés'
        EUROPEO = 'Europeo'
        PERSA = 'Persa'
        BENGALI = 'Bengalí'
        SPHYNX = 'Sphynx'


class Pet(models.Model):
    name = models.CharField(max_length=100)
    breed = models.CharField(max_length=50, choices=Breed.choices)
    birthday = models.DateField()
    weight = models.DecimalField(max_digits=20, decimal_places=2, default=0.00)

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
            weight=Decimal(pet_data.get("weight")),
        )

        return True, None

    def update_pet(self, pet_data):
        errors = validate_pet(pet_data)
        if errors:
            return False, errors

        if "name" in pet_data:
            self.name = pet_data["name"]
        if "breed" in pet_data:
            self.breed = pet_data["breed"]
        if "birthday" in pet_data:
            self.birthday = parse_date(pet_data["birthday"])
        if pet_data.get("weight"):
            self.weight = Decimal(pet_data["weight"])

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
        errors = validate_medicine(medicine_data)

        if len(errors.keys()) > 0:
            return False, errors

        self.name = medicine_data.get("name", "") or self.name
        self.description = medicine_data.get("description", "") or self.description
        self.dose = medicine_data.get("dose", "") or self.dose

        self.save()
        return True, None


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
            if int(dose) < 1 or int(dose) > 10:
                errors["dose"] = "Por favor ingrese una dosis entre 1 y 10"
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
        if price <= 0:
            errors["price"] = "Por favor ingrese un precio válido"
        elif not validate_price_format(price_str):
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
        errors = validate_product(product_data)
        if len(errors.keys()) > 0:
            return False, errors

        self.name = product_data.get("name", "") or self.name
        self.type = product_data.get("type", "") or self.type
        self.price = product_data.get("price", "") or self.price

        self.save()
