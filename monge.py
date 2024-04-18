from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
import time
import os 
# Configuración de la conexión a la base de datos de origen
bucket_origen = "viento"
url_origen = "https://eu-central-1-1.aws.cloud2.influxdata.com"
token_ = os.getenv("INFLUX_TOKEN")

# Configuración de la conexión a la base de datos de destino
url_destino = "https://eu-central-1-1.aws.cloud2.influxdata.com"
token_destino = "token_de_acceso_destino"
org_ = "f1237642dc0cea57"
bucket_destino = "shop"

# Crear clientes para la base de datos de origen y destino
cliente_origen = InfluxDBClient(url=url_origen, token=token_)
cliente_destino = InfluxDBClient(url=url_destino, token=token_)

# Obtener datos de la base de datos de origen
consulta = f'from(bucket: "{bucket_origen}") |> range(start: -1h)'  # Consulta para obtener datos recientes
resultados = cliente_origen.query_api().query(consulta, org=org_)

for table in resultados:
    for registro in table.records:
        # Obtener el nombre de la medición ('measurement') del registro
        measurement = registro.values.get('measurement', None)
        #print(registro)
        print(measurement)
        if measurement:
            # Crear un objeto Point con la medición y los campos del registro
            point = Point(measurement)
            for key, value in registro.values.items():
                if key != 'measurement':
                    point.field(key, value)
            
            # Escribir el punto en la base de datos de destino
            cliente_destino.write_api(bucket_destino, org_, point)