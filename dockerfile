# Dockerfile for Python server
FROM python:3.8-slim

# Establecer el directorio de trabajo en el contenedor
WORKDIR /usr/src/app

# Copiar el archivo de requisitos y instalar las dependencias
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto de los archivos de la aplicación
COPY . .

# Comando para ejecutar el script
CMD ["python", "-u", "index.py"]
