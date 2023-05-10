
from django.urls import path
from  .views import index,index_admin,proveedores,catalogo
from  .views import carrito, cerrar_sesion, index, iniciar_session,index_admin,proveedores, registrar_usuario,registrarse,agregar_carrito

urlpatterns =[
    path('',index,name="index"),
    path('index_admin',index_admin,name="index_admin"),
    path('proveedores',proveedores,name="proveedores"),

    path('catalogo',catalogo,name="catalogo"),

    path('registrarse',registrarse,name="registrarse"),
    path('login',iniciar_session,name="login"),
    path('carrito',carrito,name="carrito"),
    #Registro de usuario 
    path('registrar_usuario', registrar_usuario, name="registrar_usuario"),
    #Cerrar sesión
    path('cerrar_sesion/',cerrar_sesion,name ="cerrar_sesion"),
    #Agregar Carrito
    path('agregar_carrito/<int:id>/<int:precio>/',agregar_carrito,name ="agregar_carrito"),
 ]