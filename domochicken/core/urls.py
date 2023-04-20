from django.urls import path
from  .views import index, inicio_sesion,indexAdmin,proveedores

urlpatterns =[
    path('',index,name="index"),
    path('login',inicio_sesion,name="inicio_sesion"),
    path('indexAdmin',indexAdmin,name="indexAdmin"),
    path('proveedores',proveedores,name="proveedores")
 ]