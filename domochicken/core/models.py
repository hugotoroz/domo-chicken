from django.db import models
from django.contrib.auth.models import User
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
        return self.nombre_rol
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
    correo = models.CharField(max_length=50)
    direccion = models.CharField(max_length=100)
    fk_id_comuna = models.ForeignKey(Comuna,on_delete=models.CASCADE,)
    celular = models.IntegerField()
    u_is_active = models.BooleanField(default=True) 
    row_status = models.BooleanField(default=True)
    fk_id_rol = models.ForeignKey(Rol,on_delete=models.CASCADE,default=5)
    def __str__(self):
        return self.nombre_usuario
class Proveedor(models.Model):
    id_proveedor = models.BigAutoField(primary_key=True)
    nombre_proveedor = models.CharField(max_length=100)
    rut_proveedor = models.CharField(max_length=100)
    direccion = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=400)
    prov_is_active = models.BooleanField(default=True) 
    row_status = models.BooleanField(default=True)
    def __str__(self):
        return self.nombre_proveedor
class Producto(models.Model):
    id_producto = models.BigAutoField(primary_key=True)
    nombre_producto = models.CharField(max_length=100)
    stock = models.IntegerField()
    precio = models.IntegerField()
    imagenProd =models.ImageField(upload_to="productos/",default='images/Not_found.png',verbose_name="Imagen del Producto",null=True, blank=False)
    descripcion = models.CharField(max_length=400)
    fk_id_proveedor = models.ForeignKey(Proveedor,on_delete=models.CASCADE,)
    prod_is_active = models.BooleanField(default=True) 
    row_status = models.BooleanField(default=True)
    def __str__(self):
        return self.nombre_producto
class Carrito(models.Model):
    id_carrito = models.BigAutoField(primary_key=True)
    total = models.IntegerField()
    producto = models.IntegerField(null=True)
    fk_id_usuario = models.ForeignKey(User,on_delete=models.CASCADE,)
    def __str__(self):
        return self.total
class Pedido(models.Model):
    id_pedido = models.BigAutoField(primary_key=True)
    descripcion = models.CharField(max_length=400)
    fecha = models.DateTimeField()
    total = models.IntegerField()
    estado_pedido = models.TextField()
    fk_id_usuario = models.ForeignKey(Usuario,on_delete=models.CASCADE,)
    def __str__(self):
        return f"{self.id_pedido}, {self.descripcion}"
class Solicitud(models.Model):
    id_solicitud = models.BigAutoField(primary_key=True)
    cantidad_solicitud = models.IntegerField(null=True)
    estado = models.CharField(max_length=50)
    realizado_por= models.CharField(max_length=50,null=True)
    fk_id_proveedor = models.ForeignKey(Proveedor,on_delete=models.CASCADE,)
    fk_id_producto = models.ForeignKey(Producto,on_delete=models.CASCADE,)
    def __str__(self):
        return f"{self.estado} - {self.realizado_por}"
 
class ReciboPedido(models.Model):
    id_ReciboPedido = models.BigAutoField(primary_key=True)
    fk_id_usuario = models.ForeignKey(Usuario,on_delete=models.CASCADE,)
    fk_id_productos = models.ManyToManyField(Producto)
    fk_id_pedido = models.ForeignKey(Pedido,on_delete=models.CASCADE,)
    def __str__(self):
        return self.fk_id_usuario.nombre_usuario

