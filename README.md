Challenge Data Analytics - Python

Este proyecto Consume datos desde 3 fuentes distintas para popular una base de datos SQL con información sobre bibliotecas, museos y salas de cines argentinos.

Los datos de configuracion estan almacenados en .env los enlaces de las 3 fuentes y la configuración para la conexion a la base de datos PostgreSQL.

Los requerimientos necesarios para correr en un nuevo ambiente se pueden instalando los paquetes referidos en el documento requerimientos.txt.

El archivo "settings.py" contiene información pre procesada para facilitar el funcionamiento y la lectura del codigo.

El modulo "app.py" contiene todo el procesamiento de datos que: aadquiere los archivos fuentes, crea y actualiza las tablas dentro de la base de datos.

El archivo "script.py" corre 3 querys de SQL.
