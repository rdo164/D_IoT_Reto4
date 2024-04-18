from influxdb_client_3 import InfluxDBClient3, Point
from datetime import datetime
import pandas as pd
import os 

# -------------URL---------------
url = "https://eu-central-1-1.aws.cloud2.influxdata.com/api/v2/write?bucket=viento&precision=ns"

# Parámetros para la solicitud
host_ = "https://eu-central-1-1.aws.cloud2.influxdata.com"

token_ = os.getenv("INFLUX_TOKEN")


org_ = "f1237642dc0cea57"  # organización
bucket_ = "viento"  # bucket

client = InfluxDBClient3(token=token_,
                         host=host_,
                         org=org_,
                         database=bucket_)


point = Point("wind_turbine") \
    .tag("location", "site1") \
    .field("LV_ActivePower_kW", 12.45) \
    .field("Wind_Speed_ms", 90.5) \
    .field("Theoretical_Power_Curve_KWh", 90000.67) \
    .field("Wind_Direction_degrees", 0.0) \
    .time(datetime.utcnow())

client.write(point)
