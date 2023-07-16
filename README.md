## Car Rental Service Data Modeling and ETL
Este proyecto implica diseñar un modelo de datos para un servicio de renta de autos en México e implementar un proceso de ETL para generar una tabla agregada de los vehículos más reservados, incluyendo el tiempo promedio de renta. El modelo de datos está diseñado para permitir el análisis con diversas dimensiones como año, modelo, ubicación de los puntos de recogida y devolución, y otras características del vehículo.
# Data Model

Este es un modelo de datos que define la estructura de las tablas en una base de datos SQLite utilizada para almacenar información relacionada con un sistema de renta de vehículos. El modelo de datos se crea utilizando Python y la biblioteca SQLite3.

El modelo de datos incluye cuatro tablas:

vehiculos: Esta tabla almacena información sobre los vehículos disponibles para renta. La tabla tiene las siguientes columnas: id, marca, modelo, anio, tipo, capacidad, color, kilometraje y estado.

puntos_renta: Esta tabla almacena información sobre los puntos de renta disponibles. La tabla tiene las siguientes columnas: id, nombre, direccion, telefono y horario_atencion.

clientes: Esta tabla almacena información sobre los clientes que han rentado vehículos. La tabla tiene las siguientes columnas: id, nombre, correo_electronico, telefono y direccion.

rentas: Esta tabla almacena información sobre las rentas de vehículos. La tabla tiene las siguientes columnas: id, id_vehiculo, id_punto_salida, id_punto_retorno, id_cliente, fecha_inicio, fecha_fin, costo_total y duracion_renta. Además, se establecen claves foráneas que hacen referencia a las tablas vehiculos, puntos_renta y clientes.

El modelo de datos está diseñado para permitir la relación entre las diferentes tablas y para garantizar la integridad de los datos. Por ejemplo, la tabla rentas tiene claves foráneas que hacen referencia a las tablas vehiculos, puntos_renta y clientes. Esto significa que no se pueden crear registros en la tabla rentas que hagan referencia a registros que no existen en las tablas vehiculos, puntos_renta y clientes.

## Requirements

- Python 3.x
- Install requirements.txt
- Create .env file using the env.example guide.
- You can change the db name , table name using the .env file
## Usage
Se debe usar los archivos csv creados usando faker, los cuales nos permiten imitar un etl pipeline de carga de archivos cvs
```python
python run_etl.py
python tables.py
```

## Next Step
-  Se presenta una plantilla CloudFormation de AWS que se utiliza para crear una infraestructura de procesamiento de ETL utilizando AWS Batch. AWS Batch es un servicio de AWS que permite ejecutar trabajos en lote en la nube.

El archivo de plantilla crea varios recursos de AWS, incluyendo un trabajo de AWS Batch, una definición de trabajo de AWS Batch, una cola de trabajo de AWS Batch, y dos buckets de Amazon S3 para almacenar los archivos de entrada y salida.

La definición de trabajo de AWS Batch especifica los detalles del trabajo, como la imagen de Docker utilizada, la cantidad de CPU y memoria necesarias, y el comando a ejecutar. En este caso, se ejecuta un script de Python llamado run_etl.py. Además, se especifican algunas variables de entorno, como el nombre de la base de datos y los nombres de los buckets de Amazon S3 para almacenar los archivos de entrada y salida.

La cola de trabajo de AWS Batch se utiliza para organizar los trabajos en una sola ubicación y para controlar el acceso a los recursos necesarios para ejecutar los trabajos. En este caso, se especifica la prioridad de la cola y el entorno de cómputo de Batch utilizado.

El trabajo de AWS Batch se define con la definición de trabajo y la cola de trabajo. Se especifican los parámetros del trabajo, como los nombres de los archivos de entrada y salida en los buckets de Amazon S3.

Finalmente, se crean los buckets de Amazon S3 para almacenar los archivos de entrada y salida. Los nombres de los buckets se especifican en la definición de trabajo y en los parámetros del trabajo.

Para implementar la infraestructura de procesamiento de ETL utilizando AWS Batch, se puede utilizar este archivo de plantilla de AWS CloudFormation y personalizar los nombres de los buckets, la imagen de Docker, el script de Python y otros detalles según las necesidades específicas del proyecto de ETL.
## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)