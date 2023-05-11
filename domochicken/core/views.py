from django.contrib import messages
from django.shortcuts import redirect, render

from django.contrib.auth.decorators import login_required

from .models import Carrito, Comuna, Producto, Proveedor, Rol, Usuario
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User


# Create your views here.
def index(request):
    producto = Producto.objects.all()[:2]
    contexto = {'producto': producto}
    return render(request, 'index.html', contexto)


@login_required
def index_admin(request):
    usuario = Usuario.objects.filter(correo=request.user.username).first()
    contexto = {'usuario': usuario}
    return render(request, 'index_admin.html', contexto)

def agregarProd(request):
    proveedores = Proveedor.objects.all()
    contexto = {'proveedor_m': proveedores}

    return render(request, 'agregarProd.html',contexto)
#Index de modificar o eliminar producto
def modOrDeleteIndex(request):
    producto = Producto.objects.all()
    contexto = {'producto': producto}
    return render(request, 'modOrDeleteIndex.html',contexto)
#Formulario de modificacion de producto
def modificarProducto(request,idProd):
    productoM = Producto.objects.get(id_producto = idProd)
    proveedores = Proveedor.objects.all()

    return render(request, 'modificar.html',{'producto':productoM,'proveedor_m':proveedores})

def proveedores(request):

    return render(request, 'proveedores.html')

def registrarse(request):
    comunas = Comuna.objects.all()
    contexto = {"comunas_m": comunas,}
    return render(request,"registrarse.html",contexto)


def catalogo(request):

    return render(request, 'catalogo.html')


def iniciar_session(request):

    return render(request, 'login.html')


def carrito(request):

    return render(request, 'carrito.html')

def perfil(request):

    return render(request, 'perfil.html')

# FUNCIONES DE BACK END

# Función de registro de usuarios.
# Registro de usuarios


def registrar_usuario(request):
    if request.method == "POST":
        # Tomar los datos del formulario
        nom_user = request.POST['nombre']
        app_user = request.POST['apellido']
        correo = request.POST['email']
        clave = request.POST['clave']
        comuna = request.POST['comuna']
        direccion = request.POST['direccion']
        celular = request.POST['celular']
        rol = Rol.objects.get(id_rol=5)
        # Comuna que se va a insertar en la BD
        c = Comuna.objects.get(id_comuna=comuna)

        usuario = User.objects.create_user(correo, '', clave)
        # usuario.save()
        Usuario.objects.create(nombre_usuario=nom_user, apellido_usuario=app_user, celular=celular,
                               correo=correo, direccion=direccion, fk_id_rol=rol, fk_id_comuna=c)
        u_auth = authenticate(request, username=correo, password=clave)
        login(request, u_auth)
        return redirect('index')
    else:
        comunas = Comuna.objects.all()
        contexto = {'comunas': comunas}
        return render(request, 'registrarse.html', contexto)

def iniciar_sesion(request):
    if request.method == "POST":
        # Tomar los datos del formulario.
        correo = request.POST['correo']
        clave = request.POST['clave']
        # Verificar si el usuario existe
        u_auth = authenticate(request, username=correo, password=clave)
        # Tomar las credenciales del usuario
        # rol = Usuario.objects.get(correo=correo, clave=clave)
        if u_auth is not None:
            usuario = Usuario.objects.get(correo=correo)
            login(request, u_auth)
            if (usuario.fk_id_rol_id == 1):
                return redirect('index_admin')
            elif (usuario.fk_id_rol_id == 2):
                return redirect('index_admin')
            elif (usuario.fk_id_rol_id == 3):
                return redirect('index_admin')
            elif (usuario.fk_id_rol_id == 4):
                return redirect('index_admin')
            elif (usuario.fk_id_rol_id == 5):
                return redirect('index')
        else:
            messages.error(
                request, 'El usuario o la contraseÃ±a son incorrectos')
            return redirect('login')
    else:
        return render(request, 'login.html')
# Para hacer que solo pueda ingresar si es que esta logeado
# @login_required


def cerrar_sesion(request):
    logout(request)
    return redirect('login')


#Nuevo producto 
def newProd(request):
    nombre = request.POST['nomprod']
    stock = request.POST['stockprod']
    desc = request.POST['descprod']
    prove = request.POST['proveedor']
    precio = request.POST['precioprod']
    
    proveedor = Proveedor.objects.get(id_proveedor = prove)
    

    Producto.objects.create(nombre_producto = nombre,stock = stock,precio = precio,descripcion =desc,fk_id_proveedor_id = prove)
    return redirect ('index_admin')


#Modificar Producto

def editarProducto(request,idProd):
    producto = Producto.objects.get(id_producto=idProd)
    provee =request.POST['proveedor'] 
    proveedor = Proveedor.objects.get(id_proveedor = provee)
    producto.nombre_producto = request.POST.get('nomprod')
    producto.stock = request.POST.get('stockprod')
    producto.precio = request.POST.get('precioprod')
    producto.descripcion = request.POST.get('descprod')
    producto.fk_id_proveedor= proveedor
    producto.save()
    messages.success(request, '¡Producto Modificado!')
    return redirect('index_admin')

#Eliminar producto
def eliminarProducto(request, idProd):
    producto= Producto.objects.get(id_producto=idProd)
    producto.delete()

    messages.success(request, '¡Producto Eliminado!')

    return redirect('index_admin')

























""""
def agregar_carrito(request, id, precio):
    if request.user.is_authenticated:
        username_id = request.user.id
    else:
        username_id = None

    user = User.objects.get(id=username_id)

    Carrito.objects.create(total = precio,producto= id,fk_id_usuario=user)

    return redirect('carrito')

def obtener_carrito(request):
    if request.user.is_authenticated:
        username_id = request.user.id
    else:
        username_id = None

    user = User.objects.get(id=username_id)
    carrito = Carrito.objects.get(id=user)
    contexto = {'carrito': carrito}
    return render(request, 'carrito.html', contexto)


def agregar_carrito(request,producto_id,precio):
    # Obtener el usuario actual
    usuario1 = request.user.username
    usuario2= Usuario.objects.get(correo = usuario1)
    
    # Obtener el carrito del usuario actual (si existe)
    usuario3 = 3
    carrito, creado = Carrito.objects.get_or_create(fk_id_usuario=usuario1)
    
    # Agregar el producto al carrito
    carrito.fk_id_producto.add(producto_id)
    
    # Calcular el nuevo total del carrito
    carrito.total += precio
    carrito.save()
    
    # Redirigir al usuario a la página del carrito
    return redirect('carrito')
    
"""""
