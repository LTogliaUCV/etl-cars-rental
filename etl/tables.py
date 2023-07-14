import sqlite3
import os
from dotenv import load_dotenv

# Crear la conexión a la base de datos


load_dotenv()
db_name = os.getenv("RENTAL_CAR_DB")
table_vehiculos = os.getenv("VEHICULOS_TABLE")
table_clientes = os.getenv("CLIENTES_TABLE")
table_puntos_renta = os.getenv("PUNTOS_RENTA_TABLE")
table_rentas = os.getenv("RENTAS_TABLE")

conn = sqlite3.connect(db_name)
# Crear tabla de vehículos
conn.execute(f'''CREATE TABLE IF NOT EXISTS {table_vehiculos} (
    id INTEGER PRIMARY KEY,
    marca TEXT,
    modelo TEXT,
    anio INTEGER,
    tipo TEXT,
    capacidad INTEGER,
    color TEXT,
    kilometraje REAL,
    estado TEXT
)''')

# Crear tabla de puntos de renta
conn.execute(f'''CREATE TABLE  IF NOT EXISTS {table_puntos_renta} (
    id INTEGER PRIMARY KEY,
    nombre TEXT,
    direccion TEXT,
    telefono TEXT,
    horario_atencion TEXT
)''')

# Crear tabla de clientes
conn.execute(f'''CREATE TABLE IF NOT EXISTS {table_clientes} (
    id INTEGER PRIMARY KEY,
    nombre TEXT,
    correo_electronico TEXT,
    telefono TEXT,
    direccion TEXT
)''')

# Crear tabla de rentas
conn.execute(f'''CREATE TABLE IF NOT EXISTS {table_rentas} (
    id INTEGER PRIMARY KEY,
    id_vehiculo INTEGER,
    id_punto_salida INTEGER,
    id_punto_retorno INTEGER,
    id_cliente INTEGER,
    fecha_inicio TEXT,
    fecha_fin TEXT,
    costo_total REAL,
    duracion_renta TEXT,
    FOREIGN KEY (id_vehiculo) REFERENCES vehiculos(id),
    FOREIGN KEY (id_punto_salida) REFERENCES puntos_renta(id),
    FOREIGN KEY (id_punto_retorno) REFERENCES puntos_renta(id),
    FOREIGN KEY (id_cliente) REFERENCES clientes(id)
)''')


