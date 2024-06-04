import re
from datetime import datetime
from decimal import Decimal

from django.db import models


def validate_client(data):
    """"Esta funcion valida los datos que se ingresan del cliente"""
    errors = {}

    name = data.get("name", "")
    phone = data.get("phone", "")
    email = data.get("email", "")
    city = data.get("city", "")

    if name == "":
        errors["name"] = "Por favor ingrese un nombre"
    else:
        error = validate_client_char(name)
        if error is not None:
            errors["name"] = error

    if phone == "":
        errors["phone"] = "Por favor ingrese un teléfono"
    else:
        error = validate_phone_client(phone)
        if error is not None:
            errors["phone"] = error

    errorPhoneCliente= validate_int_phone_client(phone)
    if errorPhoneCliente is not None:
        errors["phone"] = errorPhoneCliente

    if email == "":
        errors["email"] = "Por favor ingrese un email"
    elif email.count("@") == 0:
        errors["email"] = "Por favor ingrese un email valido"
    elif not email.endswith("@vetsoft.com"):
        errors["email"] = "El email debe terminar con @vetsoft.com"

    if city == "" or city is None:
        errors["city"] = "Por favor ingrese una ciudad"
    elif city not in dict(CityEnum.choices):
        errors["city"] = "Ciudad no válida"

    return errors

class CityEnum(models.TextChoices):
    """Ciudades de los clientes."""
    LA_PLATA = 'La Plata',
    BERISSO = 'Berisso',
    ENSENADA = 'Ensenada',

def validate_phone_client(phone):
    """"
        esta funcion es para validar que el telefono comience con 54
    """
    # me quedo con los primeros 2 caracteres
    prefix = phone[:2]
    try:
        # convierto el prefijo a entero
        prefix = int(prefix)
        if prefix != 54:
            return "Por favor ingrese un teléfono válido"
    except ValueError:
        return "Por favor ingrese un teléfono válido"

def validate_int_phone_client(phone):
    """
        Valida que el teléfono ingresado sea un entero positivo.
    """
    if phone == "":
        return "Por favor ingrese un teléfono"
    try:
        # Convertimos phone a int
        int(phone)
    except ValueError:
        # Si la conversión falla, significa que no es entero
        return "Por favor ingrese solo valores numéricos"

def validate_client_char(name):
    """
        Valida que el nombre tenga solo letras y espacios
    """
    if re.match(r"^[A-Za-zÁÉÍÓÚáéíóúÑñ\s]+$", name):
        return None
    else:
        return "El nombre solo debe contener letras y espacios"




class Client(models.Model):
    """Modelo de cliente para los clientes de la clínica."""
    name = models.CharField(max_length=100)
    phone = models.IntegerField()
    email = models.EmailField()
    city = models.CharField(max_length=50, choices=CityEnum.choices)

    def __str__(self):
        """"
        Retorna el nombre del cliente
        """
        return self.name

    @classmethod
    def save_client(cls, client_data):
        """""
        Guarda un cliente en la base de datos
        """
        errors = validate_client(client_data)

        if len(errors.keys()) > 0:
            return False, errors

        Client.objects.create(
            name=client_data.get("name"),
            phone=client_data.get("phone"),
            email=client_data.get("email"),
            city=client_data.get("city"),
        )

        return True, None

    def update_client(self, client_data):
        """""
        Actualiza los datos de un cliente
        """

        errors = validate_client(client_data)

        if len(errors.keys()) > 0:
            return False, errors


        self.name = client_data.get("name", "") or self.name
        self.email = client_data.get("email", "") or self.email
        self.phone = client_data.get("phone", "") or self.phone
        self.city = client_data.get("city", "") or self.city

        self.save()

        return True, None




class Speciality(models.TextChoices):
    """Especialidades de los veterinarios."""
    GENERAL = "General"
    DENTISTA = "Dentista"
    TRAUMATOLOGO = "Traumatología"
    DERMATOLOGO = "Dermatología"
    CARDIOLOGO = "Cardiología"



class Vet(models.Model):
    """Modelo de veterinario para los veterinarios de la clínica."""
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    speciality = models.CharField(max_length=50, choices=Speciality.choices, default=Speciality.GENERAL)

    def __str__(self):
        return self.name

    def get_speciality_display(self):
        """"
        Retorna el nombre de la especialidad
        """
        return self.get_speciality_display()
    def formatted_phone(self):
        """"
        Retorna el teléfono formateado
        """
        return f"{self.phone[:3]}-{self.phone[3:6]}-{self.phone[6:]}"

    @classmethod
    def save_vet(cls, vet_data):
        """"
        Guarda un veterinario en la base de datos
        """
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
        """"
        Actualiza los datos de un veterinario
        """
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
    """"
    Valida los datos de un veterinario
    """
    errors = {}

    name = data.get("name", "")
    phone = data.get("phone", "")
    email = data.get("email", "")
    speciality = data.get("speciality", "")

    if name == "" or name is None:
        errors["name"] = "Por favor ingrese un nombre"


    if phone == "" or phone is None:
        errors["phone"] = "Por favor ingrese un teléfono"
    else:
        error = validate_phone(phone)
        if error is not None:
            errors["phone"] = validate_phone(phone)


    if email == "" or email is None:
        errors["email"] = "Por favor ingrese un email"
    elif email.count("@") == 0:
        errors["email"] = "Por favor ingrese un email valido"

    if speciality == "" or speciality is None:
        errors["speciality"] = "Por favor ingrese una especialidad"
    elif speciality not in dict(Speciality.choices):
        errors["speciality"] = "Especialidad no válida"

    return errors

def validate_phone(phone):
    """"Esta funcion valida el numero de telefono ingresado"""
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
    """"Esta funcion valida los datos que se ingresan del proveedor"""
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
    """Modelo de proveedor para los proveedores de la clínica."""
    name = models.CharField(max_length=100)
    email = models.EmailField()
    direccion = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    @classmethod
    def save_provider(cls, provider_data):
        """"
        Guarda un proveedor en la base de datos
        """
        errors = validate_provider(provider_data)

        if len(errors.keys()) > 0:
            return False, errors

        Provider.objects.create(
            name=provider_data.get("name"),
            email=provider_data.get("email"),
            direccion=provider_data.get("direccion"),
        )

        return True, None

    def update_provider(self, provider_data):
        """"
        Actualiza los datos de un proveedor
        """
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
    """"Esta funcion valida los datos que se ingresan de la mascota"""
    errors = {}
    # valido que el nombre no este vacio ni sea null
    name = pet_data.get("name")

    if not name or name is None:
        errors["name"] = "El nombre es requerido."
    if name == "":
        errors["name"] = "El nombre es requerido."
    # valido que la raza no este vacia ni sea null
    breed = pet_data.get("breed","")

    if breed == "" or breed is None:
        errors["breed"] = "La raza es requerida."
    elif breed not in dict(Breed.choices):
        errors["breed"] = "La raza no es válida."

    # valido que la fecha de nacimiento no este vacia ni sea null
    birthday = pet_data.get("birthday")

    if not birthday or birthday is None:
        errors["birthday"] = "La fecha de nacimiento es requerida."
    elif not parse_date(birthday):
        errors["birthday"] = "Formato de fecha incorrecto. Debe ser DD/MM/YYYY."
    if birthday == "":
        errors["birthday"] = "La fecha de nacimiento es requerida."
    # valido que el peso no este vacio ni sea null
    weight = pet_data.get("weight")

    if not weight or weight is None:
        errors["weight"] = "El peso es requerido."
    else:
        weight_error = validate_weight(weight)
        if weight_error:
            errors["weight"] = weight_error
    return errors


def validate_weight(weight):
    """"Esta funcion valida el peso ingresado de la mascota"""
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
    """"Esta funcion parsea la fecha"""
    try:
        if not date_str:
            return None
        return datetime.strptime(date_str, "%d/%m/%Y").date()
    except ValueError:
        return None  # Retorna None si hay un error en la conversión, con none se puede validar si la fecha es correcta o no


class Breed(models.TextChoices):
        """Clase enumerativa de razas de mascotas."""
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
    """Clase modelo de mascota para las mascotas de la clínica."""
    name = models.CharField(max_length=100)
    breed = models.CharField(max_length=50, choices=Breed.choices)
    birthday = models.DateField()
    weight = models.DecimalField(max_digits=20, decimal_places=2, default=0.00)

    def __str__(self):
        """"
        Retorna el nombre de la mascota
        """
        return self.name

    @classmethod
    def save_pet(cls, pet_data):
        """"
        Guarda una mascota en la base de datos
        """
        errors = validate_pet(pet_data)
        if errors:
            return False, errors

        Pet.objects.create(
            name=pet_data.get("name"),
            breed=pet_data.get("breed"),
            birthday=parse_date(pet_data.get("birthday")),
            weight=Decimal(pet_data.get("weight")),
        )
        """"
        Retorna True si no hay errores
        """
        return True, None

    def update_pet(self, pet_data):
        """"
        Actualiza los datos de una mascota
        """
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
    """Clase modelo de medicina para las medicinas de la clínica."""
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=300)
    dose = models.IntegerField()

    def __str__(self):
        """"
        Retorna el nombre del medicamento
        """
        return self.name


    @classmethod
    def save_medicine(cls, medicine_data):
        """
        Guarda un medicamento en la base de datos
        """
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
        """"

        Actualiza los datos de un medicamento
        """
        errors = validate_medicine(medicine_data)

        if len(errors.keys()) > 0:
            return False, errors

        self.name = medicine_data.get("name", "") or self.name
        self.description = medicine_data.get("description", "") or self.description
        self.dose = medicine_data.get("dose", "") or self.dose

        self.save()
        return True, None


def validate_medicine(data):
    """"Esta funcion valida los datos que se ingresan de la medicina"""
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
    """"Esta funcion valida los datos que se ingresan del producto"""
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
    """"Esta funcion valida el precio ingresado"""
    pattern = r"^\d+(\.\d+)?$"
    match = re.match(pattern, price_str)
    return match is not None


class Product(models.Model):
    """Clase modelo de producto para los productos de la clínica."""
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=50)
    price = models.FloatField(max_length=20)

    def __str__(self):
        """"
        Retorna el nombre del producto
        """
        return self.name

    @classmethod
    def save_product(cls, product_data):
        """"
        Guarda un producto en la base de datos
        """
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
        """"
        Actualiza los datos de un producto
        """
        self.name = product_data.get("name", "") or self.name
        self.type = product_data.get("type", "") or self.type
        self.price = product_data.get("price", "") or self.price

        self.save()

        return True, None
