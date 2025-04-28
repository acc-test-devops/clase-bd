# Usa una imagen base con Python
FROM python:3.9-slim

# Configura el directorio de trabajo
WORKDIR /app

# Copia los archivos al contenedor
COPY app.py db.json index.html /app/

# Instala las dependencias necesarias
RUN apt update && apt install -y procps && pip install flask

# Expone el puerto 5000
EXPOSE 5000

# Comando para ejecutar la aplicación
CMD ["python", "app.py"]
