1. Descargo e instalo influxdb en Linux
```
$ curl -O https://dl.influxdata.com/influxdb/releases/influxdb2_2.7.5-1_amd64.deb
```
```
$ sudo dpkg -i influxdb2_2.7.5-1_amd64.deb
```
2. Inicio el servicio
```
$ sudo service influxdb start
```
3. Compruebo si tengo influx instalado mediante:
```
$ influx
```
Command 'influx' not found, but can be installed with:
sudo apt install influxdb-client
Instalo al cliente con la línea que han proporcionado.

4. Crear docker-compose.yml
