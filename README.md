# D_IoT_Reto4: Persistencia de Datos

## Contexto 
- Explorar el siguiente dataset
https://www.kaggle.com/datasets/berkerisen/wind-turbine-scada-dataset

- En base a este caso de uso elegir un modelo de base de datos apropiado para gestionar una turbina de viento.

- Generar una aplicación que lea el dataset y lo inserte en la base de datos (**actualizando las marcas de tiempo**).

- Calcula diferentes tipos de agregaciones como demostración.

Extra: 

- Argumentar 
## Explicación de los pasos seguidos

### 1. Explorar el dataset para elegir el modelo de datos idóneo.

  - Para ello he creado un [jupyter notebook](./dataset/explore.ipynb) y explorado los datos que contiene el dataframe. Al ser un dataframe con tipos de dato objecto y con "pocas" columnas considero que la mejor manera de gestionar los datos sería con **Object Storage**. 

   - Al basarse en el modelo de base de datos de **series temporales** la BBDD que voy a emplear es **InfluxDB**. He de decir, que la selección se debe a su popularidad y se utiliza en la empresa que estoy actualmente. 

### 2. InfluxDB
   
1. Comprensión 
 - He leído la documentación para comprender el funcionamiento de la aplicacación.

2. Cuenta
 - He creado la cuenta de Influx, luego una organización para posteriormente poder crear el bucket.  

3. Crear el Bucket
 - He creado mi Bucket, contenedor, el cual se encargará de almacenar mis datos. Para ello me he generado un token con todos los accesos.
 He hecho una llamada POST a la API para Generar el Bucket de la siguiente manera:
 ```
 curl --silent -w "%{response_code}: %{errormsg}\n" \
  -XPOST "https://eu-central-1-1.aws.cloud2.influxdata.com/api/v2/buckets" \
  --header "Authorization: Token API_TOKEN" \
  --header "Content-type: application/json" \
  --data @- << EOF
  {
    "orgID": "ORG_ID",
    "name": "BUCKET_NAME",
    "retentionRules": [
      {
        "type": "expire",
        "everySeconds": 86400
      }
    ]
  }
EOF
```

He sustituido `API_TOKEN` por el token generado, el `ORG_ID` por el id de la organización. `BUCKET_NAME`por Wind turbine,y he dejado el parametro 86400, ya que este parametro se encarga del tiempo de almacenamiento antes de que el tiempo expire.

4. Envío de datos 

Para el envío de datos  he utilizado la siguiente línea:
```
curl --silent -w "%{response_code}: %{errormsg}\n" \
"https://eu-central-1-1.aws.cloud2.influxdata.com/api/v2/write?bucket=966ce424e102322d&precision=ns" \
-H "Authorization: Token bEF3nNWxrL_AMmFEvXXsmbd-EJcJIW2aqtXxiH4ERofqD6F-jQPhbt3H8MGBYYHOqS5laxfk3K05ZV9aCfRNfg==" \
-H "Content-Type: text/plain; charset=utf-8" \
-H "Accept: application/json" \
-d 'wind_turbine,location=site1 wind_speed=25'
```
Comprobar el envío:
```
curl -G "https://eu-central-1-1.aws.cloud2.influxdata.com/api/v2/query?org=966ce424e102322d" \
-H "Authorization: Token bEF3nNWxrL_AMmFEvXXsmbd-EJcJIW2aqtXxiH4ERofqD6F-jQPhbt3H8MGBYYHOqS5laxfk3K05ZV9aCfRNfg==" \
-H "Accept: application/csv" \
-H "Content-type: application/vnd.flux" \
-d 'org=966ce424e102322d' \
-d 'bucket=Wind turbine' \
-d 'start=-1h' \
-d 'query=from(bucket:"BUCKET_NAME") |> range(start: -1h) |> filter(fn:(r) => r._measurement == "wind_turbine")'
```
wind_turbine es la medición, location=site1 es la etiqueta del lugar y el wind_speed es el campo. Influx se encarga de añadir el timestamp en caso de que no se envie. 
> Nota: Los campos se emplean para crear informes y los tipos de datos que aceptar influxDb son Float, Integer, String, Boolean.


Si los datos se han enviado correctamente en la interfaz de InfluxDB > Data Explorer, haciendo la consulta de la imagen nos mostrará en la parte inferior los datos enviados al bucket.


![](./img_apuntes/envio_datos_terminal.png)


### 3. Generar Aplicación

https://docs.influxdata.com/influxdb/cloud-serverless/get-started/write/?t=Python





## Problemas 
- OrgID. A la hora de crear el bucket de InfluxDB estaba poniendo el nombre en vez de el id.

- Envío de datos.
  - Poner un espacio en el nombre del bucket. Lo he sustituido por %20 para poder mandar los datos
  - A la hora de postear los datos me saltaba el error `{"code":"invalid","message":"failed to parse line protocol: errors encountered on line(s):\nerror parsing line 1 (1-based): No fields were provided","line":1}` porque los datos hay que mandarlos en **nano segundos**.
  - El servidor se había quedado bloqueado, tras 4 horas, cerrand sesión y volviendo a iniciar ha funcionado a la primera.


## Bibliografía


- https://docs.influxdata.com/influxdb/cloud-serverless/api/#operation/createMeasurementSchema
