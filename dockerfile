# Usa una imagen base oficial de Python, se especifica la version exacta para evitar conflictos de versiones y en su version slim para reducir el tamaño de la imagen
FROM python:3.12-slim

# Establece el directorio de trabajo en el contenedor
WORKDIR /app

# Copia los archivos de requisitos primero para aprovechar la caché de capas de Docker
COPY requirements.txt .

# Instala las dependencias de Python necesarias
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto del código de la aplicación al contenedor
COPY . .

# Expone el puerto en el que se ejecutará la aplicación
EXPOSE 8000

# Comando para ejecutar la aplicación, ajusta según el servidor web o framework que utilices
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
