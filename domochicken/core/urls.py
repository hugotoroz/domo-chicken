from django.urls import path
from .views import solicitudes_proveedor,agregar_prov,eliminarProducto, index, index_admin, modOrDeleteIndex, modificarProducto, newProd, proveedores, catalogo, carrito, cerrar_sesion, index, iniciar_sesion, index_admin, proveedores, registrar_usuario, perfil,agregarProd, stock_productos,solicitar_stock,agregar_producto,eliminar_producto
from django.conf.urls.static import static
from django.conf import settings

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
        #Render para ver el stock
    path('stock_productos/',stock_productos,name ="stock_productos"),
    #Solicitar stock a proveedor
    path('solicitar_stock/<int:id_prod>/',solicitar_stock,name ="solicitar_stock"),
    #Render de pagina modificar o eliminar productor
    path('modificarIndex',modOrDeleteIndex,name="modOrDeleteIndex"),
    #Modificar un producto
    path('modificarProducto/<idProd>',modificarProducto,name="modificarProducto"),
    #Funcion eliminar Producto
    path('eliminarProducto/<idProd>',eliminarProducto,name="eliminarProducto"),

 #Carrito Funciones
    path('carrito/agregar/<int:id_prod>/', agregar_producto, name='agregar_producto'),
    path('carrito/eliminar/<int:id_prod>/', eliminar_producto, name='eliminar_producto'),

    path('iniciar_sesion/', iniciar_sesion, name="iniciar_sesion"),
    path('carrito', carrito, name="carrito"),
    # Registro de usuario
    path('registrar_usuario/', registrar_usuario, name="registrar_usuario"),
    # Cerrar sesión
    path('cerrar_sesion/', cerrar_sesion, name="cerrar_sesion"),
    #Solicitud a proveedores
    path('agregar_prov/', agregar_prov, name="agregar_prov"),
    #Lista de solicitudes de proveedores
    path('solicitudes_proveedor/', solicitudes_proveedor, name="solicitudes_proveedor"),
    # Agregar Carrito
    #path('agregar_carrito/<int:id>/<int:precio>/',agregar_carrito, name="agregar_carrito"),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)