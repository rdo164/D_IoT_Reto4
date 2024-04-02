# D_IoT_Reto4: Persistencia de Datos

## Contexto 
- Explorar el siguiente dataset
https://www.kaggle.com/datasets/berkerisen/wind-turbine-scada-dataset

- En base a este caso de uso elegir un modelo de base de datos apropiado para gestionar una turbina de viento.

- Generar una aplicación que lea el dataset y lo inserte en la base de datos (**actualizando las marcas de tiempo**).

- Calcula diferentes tipos de agregaciones como demostración.
---

## Explicación de los pasos seguidos

1. Explorar el dataset para elegir el modelo de datos idóneo.

    Para ello he creado un [jupyter notebook](./dataset/explore.ipynb) y explorado los datos que contiene el dataframe. Al ser un dataframe con tipos de dato objecto y con "pocas" columnas considero que la mejor manera de gestionar los datos sería con **Object Storage**
