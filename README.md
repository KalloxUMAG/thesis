# thesis

La carpeta DAGS debe ser colocada dentro de la carpeta principal de AIRFLOW.

La carpeta DAGS contiene los dags creados para la automatizacion de los scripts relacionados a cada base de datos.
Dentro de la carpeta DAGS se puede encontrar la carpeta scrips con todos los codigos utilizados.
Dentro de la carpeta DAGS se puede encontrar la carpeta files, su finalidad es almacenar los resultados generados por los codigos de la carpeta scripts y contener archivos estaticos relacionados a las bases de datos utilizadas.

Es necesario crear un archivo .env que contenga las credenciales para entablar una conexion con la base de datos. Los campos necesarios pueden ser reemplazados directamente en el archivo database.py de la carpeta db_conn.

Para obtener las interacciones de STRING es necesario descargar el archivo protein.aliases de la pagina oficial de STRING y colocarlo en su carpeta dentro de files.
