
# Dependencias y librerias
from influxdb_client_3 import InfluxDBClient3, Point
from datetime import datetime
import pandas as pd

import os

data = pd.read_csv('./dataset/T1_actualizado.csv')


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
    Date_Time, LV_ActivePower_kW, Wind_Speed_m_s,Theoretical_Power_Curv,Wind_Direction = row
    point = Point("wind_turbine") \
        .tag("location", "site1") \
        .field("LV_ActivePower_kW", LV_ActivePower_kW) \
        .field("Wind_Speed_ms",Wind_Speed_m_s ) \
        .field("Theoretical_Power_Curve_KWh", Theoretical_Power_Curv) \
        .field("Wind_Direction_degrees", Wind_Direction) \
        .time(Date_Time)
    
    client.write(point)


