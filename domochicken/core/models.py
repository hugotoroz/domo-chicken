from django.db import models

# Create your models here.
from django.db import models
# Permisos de cada usuario.
class Permiso(models.Model):
    id_permiso = models.BigAutoField(primary_key=True)
    nombre_permiso = models.CharField(max_length=40)

    def __str__(self):
        return self.nombre_permiso
# Roles de cada usuario.
class Rol(models.Model):
    id_rol = models.BigAutoField(primary_key=True)
    nombre_rol = models.CharField(max_length=30)
    fk_id_permiso = models.ForeignKey(Permiso,on_delete=models.CASCADE,)
    def __str__(self):
        return self.nombre_role_name
# Roles de cada usuario.
class Comuna(models.Model):
    id_comuna = models.BigAutoField(primary_key=True)
    comuna = models.CharField(max_length=45)
    def __str__(self):
        return self.comuna
# Los usuarios del sistema se dividirán por roles para saber si es cliente, vendedor, administrador, etc.
class Usuario(models.Model):
    id_usuario = models.BigAutoField(primary_key=True)
    nombre_usuario = models.CharField(max_length=50)
    apellido_usuario = models.CharField(max_length=50)
    celular = models.IntegerField()
    correo = models.CharField(max_length=50)
    direccion = models.CharField(max_length=100)
    clave = models.CharField(max_length=100)
    fk_id_rol = models.ForeignKey(Rol,on_delete=models.CASCADE,)
    fk_id_comuna = models.ForeignKey(Comuna,on_delete=models.CASCADE,)
    def __str__(self):
        return self.nombre_usuario
class Proveedor(models.Model):
    id_proveedor = models.BigAutoField(primary_key=True)
    nombre_proveedor = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=400)
    rut_proveedor = models.CharField(max_length=100)
    direccion = models.CharField(max_length=100)
    def __str__(self):
        return self.nombre_proveedor
class Producto(models.Model):
    id_producto = models.BigAutoField(primary_key=True)
    nombre_producto = models.CharField(max_length=100)
    stock = models.IntegerField()
    precio = models.IntegerField()
    descripcion = models.CharField(max_length=400)
    fk_id_proveedor = models.ForeignKey(Proveedor,on_delete=models.CASCADE,)
    def __str__(self):
        return self.nombre_producto
class Carrito(models.Model):
    id_carrito = models.BigAutoField(primary_key=True)
    fk_id_producto = models.ForeignKey(Producto,on_delete=models.CASCADE,)
    total = models.IntegerField()
    fk_id_usuario = models.ForeignKey(Usuario,on_delete=models.CASCADE,)
    def __str__(self):
        return self.total
class Pedido(models.Model):
    id_pedido = models.BigAutoField(primary_key=True)
    descripcion = models.CharField(max_length=400)
    fecha = models.DateTimeField()
    fk_id_usuario = models.ForeignKey(Usuario,on_delete=models.CASCADE,)
    def __str__(self):
        return self.descripcion


