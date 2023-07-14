Los requisitos necesarios para ejecutar este proyecto de manera local son los siguientes:
pip install crispy-bootstrap5
pip install Django
pip install django-crispy-forms
pip install mysqlclient
pip install Pillow
pip install pytest
pip install pytest-django
pip install requests
pip install sqlparse
pip install rut_chile

IMPORTANTE:
--> mysqlclient es solamente si utilizará la base de datos MySQL.
    -> Si vas a utilizar la base de datos por default. cambiar en settings.py la variable DATABASES a la siguiente:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
--> pytest y pytest-django es solamente si desea probar los Unit Test realizados.
--> Los demás son estrictamente necesarios para el funcionamiento.

SI SE VA A UTILIZAR LA BASE DE DATOS MYSQL POR PRIMERA VEZ:
--> Ejecutar XAMPP y crear la base de datos en phpMyAdmin primero.
--> Ejecutar MySQL Workbench y crear conexión.
--> Ingresar a la conexión y ejecutar los siguientes comandos para crear el usuario:
    -> CREATE USER 'nombre_usuario'@'localhost' IDENTIFIED BY '123';
    -> GRANT ALL PRIVILEGES ON domochicken.* TO 'nombre_usuario'@'localhost';

TARJETAS DE WEBPAY DE PRUEBA:
4051 8856 0044 6623 
AMEX 3700 0000 0002 032
CREDENCIALES
111111111
123
