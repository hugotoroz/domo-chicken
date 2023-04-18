from django.urls import path
from  .views import index, inicio_sesion

urlpatterns =[
    path('',index,name="index"),
    path('login',inicio_sesion,name="inicio_sesion"),
 ]