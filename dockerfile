# Usa una imagen base oficial de Python, se especifica la version exacta para evitar conflictos de versiones y en su version slim para reducir el tamaño de la imagen
FROM python:3.12-slim

# Establece el directorio de trabajo en el contenedor
WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Copia los archivos de requisitos primero para aprovechar la caché de capas de Docker
COPY requirements.txt .

# Instala las dependencias de Python necesarias
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt

# Copia el resto del código de la aplicación al contenedor
#COPY . .

# Expone el puerto en el que se ejecutará la aplicación
#EXPOSE 8000

# Comando para ejecutar la aplicación, ajusta según el servidor web o framework que utilices
#CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]

FROM python:3.12-slim

WORKDIR /app

COPY --from=builder /app/wheels /wheels
COPY --from=builder /app/requirements.txt .

RUN pip install --no-cache /wheels/*

COPY . .

RUN ["python", "manage.py", "migrate"]

EXPOSE 8000

CMD ["gunicorn", "--bind", ":8000", "--workers", "2", "vetsoft.wsgi"]


