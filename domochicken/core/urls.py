from django.urls import path
from .views import generar_pago,respuesta_pago,pago,error_servidor,pagina_no_encontrada,index_repartidor,modificar_usuario,agregar_usuario,modificar_proveedor,modificar_producto,agregar_producto_nuevo,eliminar_prod_cart, guardarPedido, limpiar_carrito, p_activar_producto,p_desactivar_producto,p_eliminar_producto,p_lista_productos,finalizar_solicitud, restar_producto,sp_finalizar_solicitud,sp_lista_solicitudes,activar_proveedor, desactivar_proveedor, eliminar_proveedor, p_lista_proveedores, u_lista_usuarios,activar_producto, desactivar_producto, proveedores, modificarRol, pv_activar_proveedor, pv_desactivar_proveedor, pv_eliminar_proveedor, sp_mas_info,usuarios, activar_usuario, desactivar_usuario, eliminar_usuario, solicitudes_proveedor,agregar_prov, index, index_admin, productos, proveedores, catalogo, carrito, cerrar_sesion, index, iniciar_sesion, index_admin, proveedores, registrar_usuario, perfil,editarperfil,modificarPerfil, stock_productos,solicitar_stock,agregar_producto,eliminar_producto, verPedido, webpay,commit, create, refundform,refund, ua_activar_usuario, ua_desactivar_usuario, ua_eliminar_usuario, ua_mod_rol,index_cocinero

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    #ERRORES
    path('pagina_no_encontrada', pagina_no_encontrada, name="pagina_no_encontrada"),
    path('error_servidor', error_servidor, name="error_servidor"),

    
    path('', index, name="index"),
    path('index_admin/', index_admin, name="index_admin"),
    path('proveedores/', proveedores, name="proveedores"),

    path('catalogo/', catalogo, name="catalogo"),
    
    path('perfil/', perfil, name="perfil"),
    path('editarperfil/',editarperfil,name="editarperfil"),

    path('modificarPerfil/<int:id_usuario>',modificarPerfil,name="modificarPerfil"),

    
    #Render de pagina de agregar producto
    path('agregar_producto_nuevo/',agregar_producto_nuevo,name="agregar_producto_nuevo"),
    #Render para ver el stock
    path('stock_productos/',stock_productos,name ="stock_productos"),
    #Solicitar stock a proveedor
    path('solicitar_stock/<int:id_prod>/',solicitar_stock,name ="solicitar_stock"),
    #Render de pagina modificar o eliminar productor
    path('productos/',productos,name="productos"),
    #Render de pagina modificar o eliminar proveedor
    path('proveedores',proveedores,name="proveedores"),
    path('modificar_proveedor/<id_prov>',modificar_proveedor,name="modificar_proveedor"),

    #Modificar un producto
    path('modificar_producto/<idProd>',modificar_producto,name="modificar_producto"),
    #Funciones ver usuarios admin
    path('usuarios/',usuarios,name="usuarios"),
    path('agregar_usuario/',agregar_usuario,name="agregar_usuario"),
    path('modificar_usuario/<id_user>',modificar_usuario,name="modificar_usuario"),
    #Funciones modificar rol
    path('modificarRol/<id_usuario>/',modificarRol,name="modificarRol"),
    #Funcion para desactivar un usuario
    path('desactivar_usuario/<id_usuario>/',desactivar_usuario,name="desactivar_usuario"),
    #Funcion para activar un usuario
    path('activar_usuario/<id_usuario>/',activar_usuario,name="activar_usuario"),
    #Funcion para eliminar un usuario
    path('eliminar_usuario/<id_usuario>/',eliminar_usuario,name="eliminar_usuario"),
    
    #Funciones para proveedores
    path('desactivar_proveedor/<id_proveedor>/',desactivar_proveedor,name="desactivar_proveedor"),
    path('eliminar_proveedor/<id_proveedor>/',eliminar_proveedor,name="eliminar_proveedor"),
    path('activar_proveedor/<id_proveedor>/',activar_proveedor,name="activar_proveedor"),
    path('iniciar_sesion/', iniciar_sesion, name="iniciar_sesion"),
    path('carrito/', carrito, name="carrito"),
    path('pago/', pago, name="pago"),
    path('respuesta_pago/', respuesta_pago, name="respuesta_pago"),
    path('generar_pago/', generar_pago, name="generar_pago"),
    # Registro de usuario
    path('registrar_usuario/', registrar_usuario, name="registrar_usuario"),
    # Cerrar sesión
    path('cerrar_sesion/', cerrar_sesion, name="cerrar_sesion"),
    #Solicitud a proveedores
    path('agregar_prov/', agregar_prov, name="agregar_prov"),
    #Lista de solicitudes de proveedores
    path('solicitudes_proveedor/', solicitudes_proveedor, name="solicitudes_proveedor"),
    #PEDIDOS
    path('index_repartidor/',index_repartidor,name="index_repartidor"),

    #URL MODALES
    path('sp_mas_info/<int:id_solicitud>/', sp_mas_info, name="sp_mas_info"),
    path('ua_desactivar_usuario/<int:id_usuario>/', ua_desactivar_usuario, name="ua_desactivar_usuario"),
    path('ua_activar_usuario/<int:id_usuario>/', ua_activar_usuario, name="ua_activar_usuario"),
    path('ua_eliminar_usuario/<int:id_usuario>/', ua_eliminar_usuario, name="ua_eliminar_usuario"),
    path('ua_mod_rol/<int:id_usuario>/', ua_mod_rol, name="ua_mod_rol"),
    path('pv_desactivar_proveedor/<int:id_proveedor>/', pv_desactivar_proveedor, name="pv_desactivar_proveedor"),
    path('pv_activar_proveedor/<int:id_proveedor>/', pv_activar_proveedor, name="pv_activar_proveedor"),
    path('pv_eliminar_proveedor/<int:id_proveedor>/', pv_eliminar_proveedor, name="pv_eliminar_proveedor"),
    path('lista_solicitudes', sp_lista_solicitudes, name="lista_solicitudes"),
    path('lista_usuarios/', u_lista_usuarios, name="lista_usuarios"),
    path('lista_proveedores/', p_lista_proveedores, name="lista_proveedores"),
    path('lista_productos/', p_lista_productos, name="lista_productos"),
    path('p_activar_producto/<int:id_producto>/', p_activar_producto, name="p_activar_producto"),
    path('p_desactivar_producto/<int:id_producto>/', p_desactivar_producto, name="p_desactivar_producto"),
    path('p_eliminar_producto/<int:id_producto>/', p_eliminar_producto, name="p_eliminar_producto"),
    path('sp_finalizar_solicitud/<int:id_solicitud>/', sp_finalizar_solicitud, name="sp_finalizar_solicitud"),
    path('finalizar_solicitud/<int:id_solicitud>/', finalizar_solicitud, name="finalizar_solicitud"),
    path('activar_producto/<int:id_producto>/',activar_producto,name="activar_producto"),
    path('desactivar_producto/<int:id_producto>/',desactivar_producto,name="desactivar_producto"),
    path('eliminar_producto/<int:id_producto>/',eliminar_producto,name="eliminar_producto"),

    #Seguimiento pedido


    path('seguimiento/',verPedido,name="verPedido"),
    path('guardarPedido/<int:total>/',guardarPedido,name="guardarPedido"),
    # Agregar Carrito
    path('agregar3/<int:idProducto>',agregar_producto,name="Add"),
    path('eliminar/<int:idProducto>',eliminar_prod_cart,name="Del"),
    path('restar/<int:idProducto>',restar_producto,name="Sub"),
    path('limpiar/',limpiar_carrito,name="CLS"),

    #webpay
    path('webpay/', webpay, name="webpay"),
    path('create/', create, name="create"),
    path('commit/', commit, name="commit"),
    path('refund-form/', refundform, name="refund-form"),
    path('refund/', refund, name="refund"),

    #Cocinero
    path('index_cocinero', index_cocinero, name="index_cocinero"),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)