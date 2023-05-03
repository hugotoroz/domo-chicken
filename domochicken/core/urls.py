from django.urls import path
from  .views import index, inicio_sesion,index_admin,proveedores

urlpatterns =[
    path('',index,name="index"),
    path('login',inicio_sesion,name="inicio_sesion"),
    path('index_admin',index_admin,name="index_admin"),
    path('proveedores',proveedores,name="proveedores")
 ]