import os
import psycopg2
from psycopg2.extras import RealDictCursor
from flask import Flask, request, jsonify, send_from_directory

# Crear la instancia de la aplicación Flask
app = Flask(__name__)

# Obtener la URL de la base de datos desde variables de entorno
DATABASE_URL = os.environ.get('DATABASE_URL', 'postgresql://postgres:password@db:5432/tareas_db')

# --- Funciones Auxiliares para interactuar con la base de datos ---

def get_db_connection():
    conn = psycopg2.connect(DATABASE_URL)
    conn.autocommit = True
    return conn

def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Crear tabla de tareas si no existe
    cur.execute('''
        CREATE TABLE IF NOT EXISTS tareas (
            id SERIAL PRIMARY KEY,
            descripcion TEXT NOT NULL,
            completada BOOLEAN NOT NULL DEFAULT FALSE
        )
    ''')
    
    # Verificar si hay datos existentes
    cur.execute('SELECT COUNT(*) FROM tareas')
    count = cur.fetchone()[0]
    
    # Si no hay datos, insertar datos iniciales
    if count == 0:
        cur.execute('''
            INSERT INTO tareas (descripcion, completada) VALUES
            ('Aprender Flask', FALSE),
            ('Crear API REST', FALSE),
            ('Probar Thunder Client', FALSE)
        ''')
    
    cur.close()
    conn.close()

@app.route('/')
def serve_index():
    return send_from_directory('/app', 'index.html')

# --- Endpoints API ---

# Endpoint para OBTENER TODAS las tareas (GET /tareas)
@app.route('/tareas', methods=['GET'])
def get_tareas():
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute('SELECT * FROM tareas')
    tareas = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(list(tareas))

# Endpoint para OBTENER UNA tarea por ID (GET /tareas/<id>)
@app.route('/tareas/<int:tarea_id>', methods=['GET'])
def get_tarea(tarea_id):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute('SELECT * FROM tareas WHERE id = %s', (tarea_id,))
    tarea = cur.fetchone()
    cur.close()
    conn.close()
    
    if tarea:
        return jsonify(dict(tarea))
    else:
        return jsonify({"error": "Tarea no encontrada"}), 404

# Endpoint para CREAR una nueva tarea (POST /tareas)
@app.route('/tareas', methods=['POST'])
def add_tarea():
    if not request.is_json:
        return jsonify({"error": "La solicitud debe ser JSON"}), 400

    nueva_tarea_data = request.get_json()

    if not nueva_tarea_data or 'descripcion' not in nueva_tarea_data or not nueva_tarea_data['descripcion']:
        return jsonify({"error": "Falta el campo 'descripcion' o está vacío"}), 400

    completada = nueva_tarea_data.get('completada', False)
    
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute(
        'INSERT INTO tareas (descripcion, completada) VALUES (%s, %s) RETURNING *',
        (nueva_tarea_data['descripcion'], completada)
    )
    nueva_tarea = cur.fetchone()
    cur.close()
    conn.close()

    return jsonify(dict(nueva_tarea)), 201

# --- Ejecución de la App ---
if __name__ == '__main__':
    # Inicializar la base de datos al arrancar
    init_db()
    app.run(host='0.0.0.0', port=5000)