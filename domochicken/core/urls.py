from django.urls import path
from .views import lista_usuarios,activar_producto, desactivar_producto, modificarRol, sp_mas_info,Usuario_admin, activar_usuario, desactivar_usuario, eliminar_usuario, solicitudes_proveedor,agregar_prov,eliminarProducto, index, index_admin, modOrDeleteIndex, modificarProducto, newProd, proveedores, catalogo, carrito, cerrar_sesion, index, iniciar_sesion, index_admin, proveedores, registrar_usuario, perfil,agregarProd,editarperfil,modificarPerfil, stock_productos,solicitar_stock,agregar_producto,eliminar_producto, ua_activar_usuario, ua_desactivar_usuario, ua_eliminar_usuario, ua_mod_rol
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', index, name="index"),
    path('index_admin', index_admin, name="index_admin"),
    path('proveedores', proveedores, name="proveedores"),

    path('catalogo', catalogo, name="catalogo"),
    
    path('perfil/', perfil, name="perfil"),
    path('editarperfil/',editarperfil,name="editarperfil"),

    path('modificarPerfil/<int:id_usuario>',modificarPerfil,name="modificarPerfil"),

    
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
    #Funciones ver usuarios admin
    path('Usuario_admin/',Usuario_admin,name="Usuario_admin"),
    #Funciones modificar rol
    path('modificarRol/<id_usuario>/',modificarRol,name="modificarRol"),

    path('eliminarProducto/<idProd>/',eliminarProducto,name="eliminarProducto"),
    
    #Funcion eliminar Producto
    path('activar_producto/<idProd>/',activar_producto,name="activar_producto"),
    #Funcion eliminar Producto
    path('desactivar_producto/<idProd>/',desactivar_producto,name="desactivar_producto"),
    #Funcion para desactivar un usuario
    path('desactivar_usuario/<id_usuario>/',desactivar_usuario,name="desactivar_usuario"),
    #Funcion para activar un usuario
    path('activar_usuario/<id_usuario>/',activar_usuario,name="activar_usuario"),
    #Funcion para eliminar un usuario
    path('eliminar_usuario/<id_usuario>/',eliminar_usuario,name="eliminar_usuario"),

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
    #URL MODALES
    path('sp_mas_info/<int:id_solicitud>/', sp_mas_info, name="sp_mas_info"),
    path('ua_desactivar_usuario/<int:id_usuario>/', ua_desactivar_usuario, name="ua_desactivar_usuario"),
    path('ua_activar_usuario/<int:id_usuario>/', ua_activar_usuario, name="ua_activar_usuario"),
    path('ua_eliminar_usuario/<int:id_usuario>/', ua_eliminar_usuario, name="ua_eliminar_usuario"),
    path('ua_mod_rol/<int:id_usuario>/', ua_mod_rol, name="ua_mod_rol"),
    path('lista_usuarios/', lista_usuarios, name="lista_usuarios"),

    # Agregar Carrito
    #path('agregar_carrito/<int:id>/<int:precio>/',agregar_carrito, name="agregar_carrito"),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)