import pandas as pd
import sqlite3
import logging


class RentasETL:

    def __init__(self, vehiculos_file, puntos_renta_file, clientes_file, rentas_file):
        self.vehiculos_file = vehiculos_file
        self.puntos_renta_file = puntos_renta_file
        self.clientes_file = clientes_file
        self.rentas_file = rentas_file
        self.conn = sqlite3.connect('renta_vehiculos.db')
        self.vehiculos_inserted_ids = []
        self.puntos_renta_inserted_ids = []
        self.clientes_inserted_ids = []
        self.rentas_inserted_ids = []
        logging.basicConfig(filename='rentas_etl.log', level=logging.INFO)

    def extract_vehiculos(self):
        vehiculos_df = pd.read_csv(self.vehiculos_file)
        vehiculos_df = vehiculos_df.rename(columns={
            'id_vehiculo': 'id',
            'marca': 'marca',
            'modelo': 'modelo',
            'anio': 'anio',
            'tipo': 'tipo',
            'capacidad': 'capacidad',
            'color': 'color',
            'kilometraje': 'kilometraje',
            'estado': 'estado'
        })
        vehiculos_df.name = 'vehiculos'

        # Verificar si los datos ya existen en la tabla vehiculos antes de cargarlos
        vehiculos_df = vehiculos_df.loc[~vehiculos_df['id'].isin(self.vehiculos_inserted_ids)]
        count = 0  # Inicializar contador
        for index, row in vehiculos_df.iterrows():
            id = row['id']
            cursor = self.conn.cursor()
            cursor.execute(f"SELECT COUNT(*) FROM vehiculos WHERE id = {id}")
            result = cursor.fetchone()
            if result[0] > 0:
                vehiculos_df = vehiculos_df.drop(index)
                logging.info(f"Registro duplicado en la tabla vehiculos: {row}")
            else:
                logging.info(f"Insertando registro en la tabla vehiculos: {row}")
                count += 1  # Incrementar contador en uno

        print(f"Se insertaron {count} nuevos registros en la tabla vehiculos")

        return vehiculos_df

    def extract_puntos_renta(self):
        puntos_renta_df = pd.read_csv(self.puntos_renta_file)
        puntos_renta_df = puntos_renta_df.rename(columns={
            'id_punto': 'id',
            'nombre': 'nombre',
            'direccion': 'direccion',
            'telefono': 'telefono',
            'horario_atencion': 'horario_atencion'
        })

        # Verificar si los datos ya existen en la tabla puntos_renta antes de cargarlos
        puntos_renta_df = puntos_renta_df.loc[~puntos_renta_df['id'].isin(self.puntos_renta_inserted_ids)]
        count = 0  # Inicializar contador
        for index, row in puntos_renta_df.iterrows():
            id = row['id']
            cursor = self.conn.cursor()
            cursor.execute(f"SELECT COUNT(*) FROM  puntos_renta WHERE id = {id}")
            result = cursor.fetchone()
            if result[0] > 0:
                puntos_renta_df = puntos_renta_df.drop(index)
                logging.info(f"Registro duplicado en la tabla puntos_renta: {row}")
            else:
                logging.info(f"Insertando registro en la tabla puntos_renta: {row}")
                count += 1  # Incrementar contador en uno

        print(f"Se insertaron {count} nuevos registros en la tabla puntos_renta")
        return puntos_renta_df

    def extract_clientes(self):
        clientes_df = pd.read_csv(self.clientes_file)
        clientes_df = clientes_df.rename(columns={
            'id_cliente': 'id',
            'nombre': 'nombre',
            'correo_electronico': 'correo_electronico',
            'telefono': 'telefono',
            'direccion': 'direccion'
        })
        clientes_df.name = 'clientes'

        # Verificar si los datos ya existen en la tabla clientes antes de cargarlos
        clientes_df = clientes_df.loc[~clientes_df['id'].isin(self.clientes_inserted_ids)]

        count = 0  # Inicializar contador

        for index, row in clientes_df.iterrows():
            id = row['id']
            cursor = self.conn.cursor()
            cursor.execute(f"SELECT COUNT(*) FROM clientes WHERE id = {id}")
            result = cursor.fetchone()
            if result[0] > 0:
                clientes_df = clientes_df.drop(index)
                logging.info(f"Registro duplicado en la tabla clientes: {row}")
            else:
                logging.info(f"Insertando registro en la tabla clientes: {row}")
                count += 1  # Incrementar contador en uno

        print(f"Se insertaron {count} nuevos registros en la tabla clientes")

        return clientes_df

    def extract_rentas(self):
        rentas_df = pd.read_csv(self.rentas_file)
        rentas_df = rentas_df.rename(columns={
            'id_renta': 'id',
            'id_vehiculo': 'id_vehiculo',
            'id_punto_salida': 'id_punto_salida',
            'id_punto_retorno': 'id_punto_retorno',
            'id_cliente': 'id_cliente',
            'fecha_inicio': 'fecha_inicio',
            'fecha_fin': 'fecha_fin',
            'costo_total': 'costo_total'
        })
        rentas_df.name = 'rentas'

        # Agregar columna de duración de la renta en días
        rentas_df['duracion_renta'] = (
                    pd.to_datetime(rentas_df['fecha_fin']) - pd.to_datetime(rentas_df['fecha_inicio'])).dt.days

        # Eliminar registros con duración negativa o cero
        rentas_df = rentas_df.loc[rentas_df['duracion_renta'] > 0]

        # Verificar si los datos ya existen en la tabla rentas antes de cargarlos
        rentas_df = rentas_df.loc[~rentas_df['id'].isin(self.rentas_inserted_ids)]
        count = 0  # Inicializar contador
        for index, row in rentas_df.iterrows():
            id = row['id']
            cursor = self.conn.cursor()
            cursor.execute(f"SELECT COUNT(*) FROM rentas WHERE id = {id}")
            result = cursor.fetchone()
            if result[0] > 0:
                rentas_df = rentas_df.drop(index)
                logging.info(f"Registro duplicado en la tabla rentas: {row}")
            else:
                logging.info(f"Insertando registro en la tabla rentas: {row}")
                count += 1  # Incrementar contador en uno

        print(f"Se insertaron {count} nuevos registros en la tabla rentas")
        return rentas_df

    def transform_vehiculos(self, vehiculos_df):
        vehiculos_df['marca'] = vehiculos_df['marca'].str.capitalize()
        vehiculos_df['modelo'] = vehiculos_df['modelo'].str.capitalize()
        vehiculos_df['tipo'] = vehiculos_df['tipo'].str.capitalize()
        vehiculos_df['color'] = vehiculos_df['color'].str.capitalize()
        return vehiculos_df

    def transform_puntos_renta(self, puntos_renta_df):
        puntos_renta_df['nombre'] = puntos_renta_df['nombre'].str.title()
        puntos_renta_df['direccion'] = puntos_renta_df['direccion'].str.title()
        return puntos_renta_df

    def transform_clientes(self, clientes_df):
        clientes_df['nombre'] = clientes_df['nombre'].str.title()
        clientes_df['correo_electronico'] = clientes_df['correo_electronico'].str.lower()
        clientes_df['direccion'] = clientes_df['direccion'].str.title()
        return clientes_df

    def load_vehiculos(self, vehiculos_df):
        try:
            vehiculos_df.to_sql('vehiculos', self.conn, if_exists='append', index=False)
            self.vehiculos_inserted_ids.extend(vehiculos_df['id'].tolist())
        except Exception as e:
            logging.error(f"Error al cargar la tabla vehiculos: {str(e)}")

    def load_puntos_renta(self, puntos_renta_df):
        try:
            puntos_renta_df.to_sql('puntos_renta', self.conn, if_exists='append', index=False)
            self.puntos_renta_inserted_ids.extend(puntos_renta_df['id'].tolist())
        except Exception as e:
            logging.error(f"Error al cargar la tabla puntos_renta: {str(e)}")

    def load_clientes(self, clientes_df):
        try:
            clientes_df.to_sql('clientes', self.conn, if_exists='append', index=False)
            self.clientes_inserted_ids.extend(clientes_df['id'].tolist())
        except Exception as e:
            logging.error(f"Error al cargar la tabla clientes: {str(e)}")

    def load_rentas(self, rentas_df):
        try:
            rentas_df.to_sql('rentas', self.conn, if_exists='append', index=False)
            self.rentas_inserted_ids.extend(rentas_df['id'].tolist())
        except Exception as e:
            logging.error(f"Error al cargar la tabla rentas: {str(e)}")

    def run(self):
        print("Init the Etl")
        vehiculos_df = self.extract_vehiculos()
        puntos_renta_df = self.extract_puntos_renta()
        clientes_df = self.extract_clientes()
        rentas_df = self.extract_rentas()

        vehiculos_df = self.transform_vehiculos(vehiculos_df)
        puntos_renta_df = self.transform_puntos_renta(puntos_renta_df)
        clientes_df = self.transform_clientes(clientes_df)

        self.load_vehiculos(vehiculos_df)
        self.load_puntos_renta(puntos_renta_df)
        self.load_clientes(clientes_df)
        self.load_rentas(rentas_df)

        self.conn.commit()
        self.conn.close()