# Dependencias y librerias
from influxdb_client_3 import InfluxDBClient3, Point
import datetime
import pandas as pd

import os

data = pd.read_csv('./dataset/T1.csv')

def actualizar_fechas_y_guardar_csv(data, nombre_archivo):
    fecha_actual = datetime.datetime.now().date()
    # Convertir la columna 'Date/Time' a datetime
    data['Date/Time'] = pd.to_datetime(data['Date/Time'], format='%d %m %Y %H:%M')
    # Reemplazar las fechas en la columna 'Date/Time' con la fecha actual
    data['Date/Time'] = data['Date/Time'].apply(
        lambda dt: dt.replace(year=fecha_actual.year, month=fecha_actual.month, day=fecha_actual.day)
    )

    #data = data.drop_duplicates(subset=['Date/Time'])
    data.to_csv(nombre_archivo, index=False)



actualizar_fechas_y_guardar_csv(data, 'T1_actualizado.csv')

# Parámetros para la solicitud
host_ = "https://eu-central-1-1.aws.cloud2.influxdata.com"
token_ = os.getenv("INFLUX_TOKEN")

org_ = "f1237642dc0cea57"  # La organización
bucket_ = "viento"  # El bucket

client = InfluxDBClient3(token=token_,
                         host=host_,
                         org=org_,
                         database=bucket_)


for index, row in data.iterrows():
    
    #if index < 144:
        
        Date_Time, LV_ActivePower_kW, Wind_Speed_m_s,Theoretical_Power_Curv,Wind_Direction = row

        point = Point("wind_turbine") \
            .tag("location", "site1") \
            .field("LV_ActivePower_kW", LV_ActivePower_kW) \
            .field("Wind_Speed_ms",Wind_Speed_m_s ) \
            .field("Theoretical_Power_Curve_KWh", Theoretical_Power_Curv) \
            .field("Wind_Direction_degrees", Wind_Direction) \
            .time(Date_Time)
        
        client.write(point)

