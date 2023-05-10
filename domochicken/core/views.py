from django.shortcuts import render
from .models import Permiso

# Create your views here.
def index(request):
    
    return render(request, 'index.html')
    
def inicio_sesion(request):

    return render(request,'inicio_sesion.html')

def index_admin(request):

    return render(request,'index_admin.html')

def proveedores(request):

    return render(request,'proveedores.html' )

def catalogo(request):

    return render(request,'catalogo.html')


    