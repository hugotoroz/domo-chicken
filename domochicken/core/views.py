from django.shortcuts import render
from .models import Permiso

# Create your views here.
def index(request):
    tu_variable = Permiso.objects.get()
    return render(request, 'index.html', {'nombre_permiso': tu_variable.nombre_permiso})
    
def inicio_sesion(request):

    return render(request,'inicio_sesion.html')

def index_admin(request):

    return render(request,'index_admin.html')

def proveedores(request):

    return render(request,'proveedores.html' )



    