# D_IoT_Reto4: Persistencia de Datos

## Contexto 

- Explorar el siguiente dataset
https://www.kaggle.com/datasets/berkerisen/wind-turbine-scada-dataset

- En base a este caso de uso elegir un modelo de base de datos apropiado para gestionar una turbina de viento.

- Generar una aplicación que lea el dataset y lo inserte en la base de datos (**actualizando las marcas de tiempo**).

- Calcula diferentes tipos de agregaciones como demostración.

Extra: 

- Demostrar mediante una visualización la inserción de datos correcta

- Argumentar la BBDD 

- Introducir seguridad

# Explicación de los pasos seguidos

## 1. Explorar el dataset para elegir el modelo de datos idóneo.

  - Para ello he creado un [jupyter notebook](./dataset/explore.ipynb) y explorado los datos que contiene el dataframe. Al ser un dataframe con tipos de dato objecto y con un formato .csv, considero que la mejor manera de gestionar los datos sería con una BBDD **NoSQL**. 

   - Al basarse en el modelo de base de datos de **series temporales** la BBDD que voy a emplear es  **InfluxDB**. He de decir, que la selección se debe a su popularidad y se utiliza en la empresa que estoy actualmente. 

## 2. InfluxDB
   
### 1. Comprensión 
 - He leído la documentación para comprender el funcionamiento de la aplicacación.

### 2. Cuenta
 - He creado la cuenta de Influx, luego una organización para posteriormente poder crear el bucket.  

### 3. Crear el Bucket

 - He creado mi Bucket, contenedor, el cual se encargará de almacenar mis datos. Para ello me he generado un token con todos los accesos.
 He hecho una llamada POST a la API para Generar el Bucket de la siguiente manera:
```
  curl --silent -w "%{response_code}: %{errormsg}\n" \
  -XPOST "https://eu-central-1-1.aws.cloud2.influxdata.com/api/v2/buckets" \
  --header "Authorization: Token MI_TOKEN"\
  --header "Content-type: application/json" \
  --data @- << EOF
{
    "orgID": "f1237642dc0cea57",
  "name": "viento",
    
    "retentionRules": [
      {
        "type": "expire",
      "everySeconds": 86400
      }
    ]
  }
EOF
```

  He sustituido `API_TOKEN` por el token generado, el `ORG_ID` por el id de la organización. `BUCKET_NAME` por wind_turbine,y he dejado el parametro 86400, ya que este parametro se encarga del tiempo de almacenamiento antes de que el tiempo expire.

### 4. Envío de datos 

  #### 1 Línea de comandos

  Para el envío de datos, lo he hecho enviando un dato desde la línea de comandos con la siguiente línea:
  ```
  curl --silent -w "%{response_code}: %{errormsg}\n" \
  "https://eu-central-1-1.aws.cloud2.influxdata.com/api/v2/write?bucket=966ce424e102322d&precision=ns" \
  -H "Authorization: Token MI_TOKEN
  -H "Content-Type: text/plain; charset=utf-8" \
  -H "Accept: application/json" \
  -d 'wind_turbine,location=site1 wind_speed=25'
  ```
  Al ejecutar el comando devuelve un 201, informando de que la consulta ha sido enviada correctamente.
  
  wind_turbine es la medición, location=site1 es la etiqueta del lugar y el wind_speed es el campo. 
  Influx se encarga de añadir el **timestamp** en caso de que **no** se **envie**. 

  > Nota: Los campos se emplean para crear informes y los tipos de datos que aceptar influxDb son Float, Integer, String, Boolean.

#### 2 **Envío de datos** desde un **Script**

  Una vez conseguido el envío de datos voy a envíar datos desde un script de python: 
```
from influxdb_client_3 import InfluxDBClient3, Point
from datetime import datetime
import pandas as pd

# -------------URL DEL CLOUD---------------
url = "https://eu-central-1-1.aws.cloud2.influxdata.com/api/v2/write?bucket=viento&precision=ns"

# Parámetros para la solicitud
host_ = "https://eu-central-1-1.aws.cloud2.influxdata.com"
token_ = MI_TOKEN
org_ = "f1237642dc0cea57"
bucket_ = "viento"  

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
```
  -  Si los datos se han enviado correctamente en la interfaz de InfluxDB > Data Explorer, haciendo la consulta de la imagen nos mostrará en la parte inferior los datos enviados al bucket.

  ![](./img_apuntes/envio_datos_terminal.png) 


### 3. Generar Aplicación

A la hora de generar la aplicación he pensado en hacerlo de la siguiente manera:

1. Actualizar la fecha tiempo

En la sección de **Actualizar Fecha tiempo** de [explore](./dataset/explore.ipynb) he hecho el ajuste.
Como hay que actualizar las fechas porque son de 2018, he pensado en **actualizar el año** simplemente. Así, una vez cambiadas generar otro y otro archivo .csv  y almacenarlo para no perder la fuente de datos original. 

2. Recorrer el dataframe 
En la sección de **Lectura del dataframe** de [explore](./dataset/explore.ipynb) he comprobado cómo iterar el dataframe.

Ahora con el dataframe actualizado, voy comprobar cómo recorrerlo con el siguiente código:

```
import pandas as pd

data = pd.read_csv('T1_actualizado.csv')

for index, row in data.iterrows():
    print(index)
    #print(row)

    Date_Time, LV_ActivePower_kW, Wind_Speed_m_s,Theoretical_Power_Curv,Wind_Direction = row
    print(Date_Time)
    print( LV_ActivePower_kW)
    print(Wind_Speed_m_s)
    print("-----")
    print( Theoretical_Power_Curv)
    print( Wind_Direction)

    input()
```

3. Envío de datos iterados 

Para el envío de datos simplemente he creado el script [iterate_write.py](./iterate_write.py),  modificando el [código anterior](./README.md/#2-envío-de-datos-desde-un-script) y recorriendo el .csv generado. Quedando de la siguiente manera:

```

# Dependencias y librerias
from influxdb_client_3 import InfluxDBClient3, Point
from datetime import datetime
import pandas as pd


data = pd.read_csv('./dataset/T1_actualizado.csv')


# Parámetros para la solicitud
host_ = "https://eu-central-1-1.aws.cloud2.influxdata.com"
token_ = MI_TOKEN

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

```

### Seguridad: VARIABLE DE ENTORNO

He creado una variable de entorno para utilizar y proporcionar buenas prácticas, ya que en caso de que cualquiere usuario tenga acceso al repositorio podría publicar datos en mi bucket.

Para la creación de mi variable de entorno, desde la terminal de WSL he seguido los siguientes comandos:
```
export INFLUX_TOKEN=VALOR_TOKEN
``` 

He comprobado que se haya creado la variable mediante:
``` 
printenv
``` 

He almacenado permanentemente el valor de la variable editando mi archivo bashrc
``` 
nano ~/.bashrc
``` 

y he añadido 
```
export INFLUX_TOKEN=VALOR_DE_MI_TOKEN
```

Después he abierto otra terminal y he utilizado el printenv para comprobar que lo he creado correctamente.
Y para utilizarlo en mi código simplemente he importado la librería os y el siguiente código 

```
import os 

...

token = os.getenv("INFLUX_TOKEN")
```

## Mejoras 
- Procesamiento de datos: comprobar si los datos son correctos y si no están repetidos
- Añadir fuente de datos
- Automatización de la ingesta de datos
- Añadir seguridad TSL/SSL

## Problemas 
- OrgID. A la hora de crear el bucket de InfluxDB estaba poniendo el nombre en vez de el id.

- Envío de datos.
  - Poner un espacio en el nombre del bucket. Lo he sustituido por %20 para poder mandar los datos
  - A la hora de postear los datos me saltaba el error `{"code":"invalid","message":"failed to parse line protocol: errors encountered on line(s):\nerror parsing line 1 (1-based): No fields were provided","line":1}` porque los datos hay que mandarlos en **nano segundos**.
  - El servidor se había quedado bloqueado, tras 4 horas, cerrando sesión y volviendo a iniciar ha funcionado a la primera.
- Bibliotecas

## Alternativas

- Prometheus: es una BBDD de que tiene la capacidad de controlar grandes volumenes de series temporales.
- Elastic Search, Filebeat y Kibana: En caso de que los datos fueran obtenidos en tiempo real se podría hacer automaticamente con Docker como hice en el Reto 1.