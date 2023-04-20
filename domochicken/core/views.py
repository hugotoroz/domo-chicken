from django.shortcuts import render

# Create your views here.
def index(request):

    return render(request,'index.html')
    
def inicio_sesion(request):

    return render(request,'inicio_sesion.html')

def indexAdmin(request):

    return render(request,'indexAdmin.html')

def proveedores(request):

    return render(request,'proveedores.html' )