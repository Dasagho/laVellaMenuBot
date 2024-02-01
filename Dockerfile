# Usar Python 3.12 como imagen base
FROM python:3.12

# Establecer el directorio de trabajo en el contenedor
WORKDIR /app

# Copiar el directorio actual en el contenedor en /app
COPY . /app

# Instalar las dependencias del fichero dependencies.txt
RUN pip install --no-cache-dir -r dependencies.txt

# Comando para ejecutar la aplicación
CMD ["python", "main.py"]
