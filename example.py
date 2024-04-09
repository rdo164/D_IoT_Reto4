from influxdb_client import InfluxDBClient
from datetime import datetime

#client = InfluxDBClient('localhost', 8086, 'admin', 'Password1', 'mydb')

token = "2xxsXIxgVCwPznjv3VRMTqdm2o5Nm31NK5dLBdcf189KH3RHHmEjNuHH5_6AnBvF44jA8t_59XN966iBbXK6MQ=="  # Tu token de acceso
org = "f1237642dc0cea57"  # Tu organización
bucket = "viento"  # Tu bucket
#url = "https://eu-central-1-1.aws.cloud2.influxdata.com/api/v2/write?bucket=viento&precision=ns"

client = InfluxDBClient(url='localhost:8086', token=token, org=org)

json_payload = []

data = {
    "measurement": "stocks",
    "tags": {
        "ticker": "TSLA" 
        },
    "time": datetime.now(),
    "fields": {
        'open': 688.37,
        'close': 667.93
    }
}
json_payload.append(data)

client.write_api(json_payload)


client.create_database('Viento')
client.get_list_database()
client.switch_database('Viento')