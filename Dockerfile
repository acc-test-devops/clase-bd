# Usa una imagen base con Python
FROM python:3.9-slim

# Configura el directorio de trabajo
WORKDIR /app

# Copia los archivos al contenedor
COPY app.py index.html /app/

# Instala las dependencias necesarias
RUN apt update && apt install -y procps gcc libpq-dev && \
    pip install flask psycopg2-binary

# Expone el puerto 5000
EXPOSE 5000

# Comando para ejecutar la aplicación
CMD ["python", "app.py"]