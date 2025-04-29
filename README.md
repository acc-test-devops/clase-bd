# 1. Crear una red para comunicación entre contenedores
podman network create tareas_network

# 2. Iniciar contenedor de PostgreSQL
podman run -d --name db --network tareas_network -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=password -e POSTGRES_DB=tareas_db -v postgres_data:/var/lib/postgresql/data -p 5432:5432 postgres:13

# 3. Construir la imagen de la aplicación web
podman build -t tareas-app .

# 4. Iniciar contenedor de la aplicación web
podman run -d --name web --network tareas_network -e DATABASE_URL=postgresql://postgres:password@db:5432/tareas_db -v ./:/app -p 5000:5000 tareas-app