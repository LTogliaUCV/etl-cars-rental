import sqlite3

# Crear la conexión a la base de datos
conn = sqlite3.connect('renta_vehiculos.db')

# Crear tabla de vehículos
conn.execute('''CREATE TABLE IF NOT EXISTS vehiculos (
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
conn.execute('''CREATE TABLE  IF NOT EXISTS puntos_renta (
    id INTEGER PRIMARY KEY,
    nombre TEXT,
    direccion TEXT,
    telefono TEXT,
    horario_atencion TEXT
)''')

# Crear tabla de clientes
conn.execute('''CREATE TABLE IF NOT EXISTS clientes (
    id INTEGER PRIMARY KEY,
    nombre TEXT,
    correo_electronico TEXT,
    telefono TEXT,
    direccion TEXT
)''')

# Crear tabla de rentas
conn.execute('''CREATE TABLE IF NOT EXISTS rentas (
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

# Extraer datos relevantes de las tablas de vehículos y rentas
query = '''SELECT v.id, v.marca, v.modelo, v.anio, v.tipo, v.capacidad, COUNT(*) AS num_rentas
FROM vehiculos v
INNER JOIN rentas r ON v.id = r.id_vehiculo
WHERE r.fecha_inicio >= date('now', '-1 year')
GROUP BY v.id, v.marca, v.modelo, v.anio, v.tipo, v.capacidad'''

result1 = conn.execute(query).fetchall()

# Calcular el tiempo promedio de renta para cada vehículo
query = '''SELECT r.id_vehiculo, AVG(julianday(r.fecha_fin) - julianday(r.fecha_inicio)) AS duracion_promedio
FROM rentas r
GROUP BY r.id_vehiculo'''

result2 = conn.execute(query).fetchall()

# Agregar los datos a una tabla agregada
query = '''SELECT v.id, v.marca, v.modelo, v.anio, v.tipo, v.capacidad, COUNT(*) AS num_rentas, AVG(julianday(r.fecha_fin) - julianday(r.fecha_inicio)) AS duracion_promedio
FROM vehiculos v
INNER JOIN rentas r ON v.id = r.id_vehiculo
WHERE r.fecha_inicio >= date('now', '-1 year')
GROUP BY v.id, v.marca, v.modelo, v.anio, v.tipo, v.capacidad'''

result3 = conn.execute(query).fetchall()

# Utilizar esta tabla agregada para realizar análisis con diversas dimensiones
query = '''SELECT marca, modelo, anio, tipo, capacidad, num_rentas, duracion_promedio
FROM (
    SELECT v.id, v.marca, v.modelo, v.anio, v.tipo, v.capacidad, COUNT(*) AS num_rentas, AVG(julianday(r.fecha_fin) - julianday(r.fecha_inicio)) AS duracion_promedio
    FROM vehiculos v
    INNER JOIN rentas r ON v.id = r.id_vehiculo
    WHERE r.fecha_inicio >= date('now', '-1 year')
    GROUP BY v.id, v.marca, v.modelo, v.anio, v.tipo, v.capacidad
) AS tabla_agregada
ORDER BY num_rentas DESC, duracion_promedio ASC'''

result4 = conn.execute(query).fetchall()

# Cerrar la conexión a la base de datos
conn.close()