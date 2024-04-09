from influxdb_client_3 import InfluxDBClient3, Point
from datetime import datetime
import pandas as pd
# -------------URL---------------
url = "https://eu-central-1-1.aws.cloud2.influxdata.com/api/v2/write?bucket=viento&precision=ns"
ruta = './dataset/T1_actualizado.csv'
data = pd.read_csv(ruta)

# Parámetros para la solicitud
host_ = "https://eu-central-1-1.aws.cloud2.influxdata.com"
token_ = "2xxsXIxgVCwPznjv3VRMTqdm2o5Nm31NK5dLBdcf189KH3RHHmEjNuHH5_6AnBvF44jA8t_59XN966iBbXK6MQ=="  # Tu token de acceso
org_ = "f1237642dc0cea57"  # Tu organización
bucket_ = "viento"  # Tu bucket

client = InfluxDBClient3(token=token_,
                         host=host_,
                         org=org_,
                         database=bucket_)


point = Point("wind_turbine") \
    .tag("location", "site1") \
    .field("LV_ActivePower_kW", 1223.45) \
    .field("Wind_Speed_ms", 10.5) \
    .field("Theoretical_Power_Curve_KWh", 250.67) \
    .field("Wind_Direction_degrees", 0.0) \
    .time(datetime.utcnow())

client.write(point)
