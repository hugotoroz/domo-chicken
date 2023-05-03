1.Ejecutar XAMPP y crear la base de datos en phpMyAdmin primero.
2.Ejecutar MySQL Workbench y crear conexión.
3. Ingresar a la conexión y ejecutar los siguientes comandos para crear el usuario:
    CREATE USER 'nombre_usuario'@'localhost' IDENTIFIED BY '123';
    GRANT ALL PRIVILEGES ON domochicken.* TO 'nombre_usuario'@'localhost';