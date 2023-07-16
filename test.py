import unittest
import sqlite3
import pandas as pd


class TestRentas(unittest.TestCase):
    def select_data(table_name):
        # Select all data from the data table and return it as a Pandas DataFrame
        conn = sqlite3.connect('renta_vehiculos.db')
        select_query = f"SELECT * FROM {table_name}"
        df = pd.read_sql(select_query, conn)
        conn.close()
        return df

    def test_ddl(self):
        # Crear una conexión a la base de datos
        conn = sqlite3.connect('renta_vehiculos.db')

        # Obtener el DDL para cada tabla en la base de datos
        cursor = conn.cursor()
        cursor.execute("SELECT sql FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()

        # Mostrar el DDL de cada tabla
        for table in tables:
            print(table[0])
            print("\n")

        # Cerrar la conexión a la base de datos
        conn.close()

    def test_select_data(self):
        # Seleccionar todos los datos de la tabla 'clientes'
        df = TestRentas.select_data('clientes')

        # Verificar que se obtuvo un DataFrame no vacío
        self.assertFalse(df.empty)

        # Verificar que el DataFrame tiene todas las columnas esperadas
        expected_columns = ['id', 'nombre', 'correo_electronico', 'telefono', 'direccion']
        self.assertListEqual(list(df.columns), expected_columns)


if __name__ == '__main__':
    unittest.main()