
from django.urls import path
from .views import eliminarProducto, index, index_admin, modOrDeleteIndex, modificarProducto, newProd, proveedores, catalogo, carrito, cerrar_sesion, index, iniciar_sesion, index_admin, proveedores, registrar_usuario, perfil,agregarProd


urlpatterns = [
    path('', index, name="index"),
    path('index_admin', index_admin, name="index_admin"),
    path('proveedores', proveedores, name="proveedores"),

    path('catalogo', catalogo, name="catalogo"),

    path('perfil/', perfil, name="perfil"),
    
    #Render de pagina de agregar producto
    path('agregarProd',agregarProd,name="agregarProd"),
    #Funcion de agregar producto
    path('agregarProd2/',newProd,name ="addProd"),
    #Render de pagina modificar o eliminar productor
    path('modificarIndex',modOrDeleteIndex,name="modOrDeleteIndex"),
    #Modificar un producto
    path('modificarProducto/<idProd>',modificarProducto,name="modificarProducto"),
    #Funcion eliminar Producto
    path('eliminarProducto/<idProd>',eliminarProducto,name="eliminarProducto"),



    path('iniciar_sesion/', iniciar_sesion, name="iniciar_sesion"),
    path('carrito', carrito, name="carrito"),
    # Registro de usuario
    path('registrar_usuario/', registrar_usuario, name="registrar_usuario"),
    # Cerrar sesión
    path('cerrar_sesion/', cerrar_sesion, name="cerrar_sesion"),
    # Agregar Carrito
    #path('agregar_carrito/<int:id>/<int:precio>/',agregar_carrito, name="agregar_carrito"),
]
