from django.contrib import admin

from .models import Usuario,Producto,Proveedor,Pedido,Permiso,Carrito,Comuna,Rol,Solicitud
# Register your models here.

admin.site.register(Usuario)
admin.site.register(Producto)
admin.site.register(Proveedor)
admin.site.register(Pedido)
admin.site.register(Permiso)
admin.site.register(Carrito)
admin.site.register(Comuna)
admin.site.register(Rol)
admin.site.register(Solicitud)