# apiRest_python
API REST desarrollada con Python-FastAPI y PostgreSQL
===========================================================================
En el devcontainer se encuentra un dockerfile que añade la instalación del cliente de Postgres, dentro del docker-compose se incluyen las credenciales de la base de datos:

[DBHOST=localhost
DBUSER=postgres
DBPASS=postgres
DBNAME=postgres]

Y en el devcontainer.json se incluyeron las customizations, donde se añadieron los id de las extensiones usadas durante el desarrollo.

===========================================================================

**Pasos para la generación del entorno virtual en caso de que esté corrupto:**

1.- Abrir la terminal

2.- Cambiarse a la carpeta app _[cd app]_
 
3.- Escribir en la terminal el comando para la creación del entorno virtual: _[python3 -m venv venv]_
 
4.- Instalar las dependencias del archivo requirements.txt: _[pip install -r ../requirements.txt]_
 
5.- Activar el entorno virtual: _[source venv/bin/activate]_


**NOTAS IMPORTANTES: **
* Para desactivar el entorno virtual ejecutar el comando: _[deactivate]_
* El entorno virtual debe crearse dentro de la misma carpeta que el archivo base de la API **[main.py]**
* Se puede activar el entorno virtual fuera de la carpeta app, pero se tiene que seguir el mismo procedimiento de: _[source rutaDelEntornoVirtual/bin/activate]_

===========================================================================

**DATOS A TOMAR EN CUENTA**

* Las dependencias se instalan una vez activando el entorno virtual, si no se instalan en el entorno virtual no se podrá ejecutar la API ni contará con las respectivas dependencias.
* Al instalar las dependencias en el entorno virtual, para poder ejecutar la API se deberá posicionar en la carpeta **[app]** e introducir el comando de activación por medio de uvicorn: _[uvicorn main:app --reload]_
* El argumento _--reload_ sirve para que cada vez que se haga una modificación al código, estando la API activa, se cargarán los cambios en el instante.

===========================================================================

**POSTGRES DESDE BASH**

Para usar postgres desde el bash se puede acceder por medio de el siguiente comando:

_[psql -U postgres -W -h localhost]_

Con el comando anterior, por medio del argumento -U indicamos el usuario(postgres) con -W indicamos que requiere de contraseña(postgres) y con -h le mencionamos el host(localhost).
_NOTA_: Para mayor información de postgres ejecutar el comando _[psql --help]_

Una vez conectado, dejo a continuación comandos básicos de postgres:
* \l muestra las bases de datos disponibles
* \q permite salir del cliente de postgres
* \c permite conectarse a la bd por defecto "postgres"

Una vez conectado a la bd por defecto, se pueden ejecutar sentencias de SQL, ya sean creaciones de tablas, inserts, updates, deletes, etcétera.
_NOTA IMPORTANTE:_ Para poder indicarle al cliente de postgres que ya se terminó la sentencia, es necesario ingresar un _;_ al final
