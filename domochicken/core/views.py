from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import Carrito, Comuna, Producto, Proveedor, Rol, Usuario
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User


def role_required(role):
    def check_role(user):
        return user.is_authenticated and Usuario.objects.filter(fk_id_rol=role).exists()

    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            if not check_role(request.user):
                # redirigir a la página principal
                return redirect(reverse('index'))
            return view_func(request, *args, **kwargs)
        return wrapper

    return decorator


def index(request):
    producto = Producto.objects.all()[:3]
    usuario = Usuario.objects.filter(correo=request.user.username).first()
    contexto = {'producto': producto}
    return render(request, 'index.html', contexto)


@login_required(login_url="iniciar_sesion/")
# @role_required('1')
# @role_required('2')
# @role_required('3')
# @role_required('4')
def index_admin(request):
    usuario = Usuario.objects.filter(correo=request.user.username).first()
    contexto = {'usuario': usuario}
    return render(request, 'index_admin.html', contexto)


def agregarProd(request):
    proveedores = Proveedor.objects.all()
    contexto = {'proveedor_m': proveedores}

    return render(request, 'agregarProd.html', contexto)
# Index de modificar o eliminar producto


@login_required(login_url="iniciar_sesion/")
def modOrDeleteIndex(request):
    producto = Producto.objects.all()
    contexto = {'producto': producto}
    return render(request, 'modOrDeleteIndex.html', contexto)


#Pagina de stockIndex
@login_required(login_url="iniciar_sesion/")
def stockIndex(request):
    producto = Producto.objects.all()
    contexto = {'producto': producto}
    return render(request, 'stock.html', contexto)

#Formulario para solicitar stock
@login_required(login_url="iniciar_sesion/")
def stockSolicitar(request,id_prod):
    producto = Producto.objects.get(id_producto = id_prod)
    contexto = {'producto': producto}
    return render(request, 'pedirStock.html', contexto)

#Funcion para el solicitar stock
def pedirStock(request,id_prod):
    if request.method == "POST":
        cantidad = int(request.POST['cantidad'])
        producto = Producto.objects.get(id_producto = id_prod)
        producto.stock += cantidad
        producto.save()
        return redirect('stockIndex')




# Formulario de modificacion de producto
@login_required(login_url="iniciar_sesion/")
def modificarProducto(request, idProd):
    if request.method == "POST":
        producto = Producto.objects.get(id_producto=idProd)
        provee = request.POST['proveedor']
        proveedor = Proveedor.objects.get(id_proveedor=provee)
        producto.nombre_producto = request.POST.get('nomprod')
        producto.stock = request.POST.get('stockprod')
        producto.precio = request.POST.get('precioprod')
        producto.descripcion = request.POST.get('descprod')
        producto.fk_id_proveedor = proveedor
        producto.save()
        messages.success(request, '¡Producto Modificado!')
        return redirect('index_admin')

    else:
        productoM = Producto.objects.get(id_producto=idProd)
        proveedores = Proveedor.objects.all()
        return render(request, 'modificar.html', {'producto': productoM, 'proveedor_m': proveedores})


@login_required(login_url="iniciar_sesion/")
def proveedores(request):
    return render(request, 'proveedores.html')


def catalogo(request):

    return render(request, 'catalogo.html')


def iniciar_session(request):

    return render(request, 'login.html')


def carrito(request):
    if request.user.is_authenticated:
        usuario = request.user
        carrito = Carrito.objects.filter(fk_id_usuario_id = usuario.id).order_by('fk_id_usuario_id').first()
        productoCarrito = Producto.objects.filter(id_producto__in = carrito.fk_id_producto_id.all())
        
        
        return render(request, 'carrito.html',{'productos': productoCarrito})
    else:
        return redirect('login')

@login_required(login_url="iniciar_sesion/")
def perfil(request):
    usuario = Usuario.objects.filter(correo=request.user.username).first()
    contexto = {'usuario': usuario}
    return render(request, 'perfil.html', contexto)

# Registro de usuarios.


def registrar_usuario(request):
    if request.method == "POST":
        # Tomar los datos del formulario
        nom_user = request.POST['nombre']
        app_user = request.POST['apellido']
        correo = request.POST['correo']
        clave = request.POST['clave']
        comuna = request.POST['comuna']
        direccion = request.POST['direccion']
        celular = request.POST['celular']
        # Validar si el usuario existe en la base de datos.
        existe_usuario = False
        
        if Usuario.objects.filter(correo=correo).exists():
            messages.success(request, 'El correo ya está registrado.')
            return redirect('registrar_usuario')
        else:
            # Rol que se va a insertar en la BD
            rol = Rol.objects.get(id_rol=5)
            # Comuna que se va a insertar en la BD
            c = Comuna.objects.get(id_comuna=comuna)
            usuario = User.objects.create_user(correo, '', clave)

            Usuario.objects.create(nombre_usuario=nom_user, apellido_usuario=app_user, celular=celular,
                                   correo=correo, direccion=direccion, fk_id_rol=rol, fk_id_comuna=c)
            u_auth = authenticate(request, username=correo, password=clave)
            ##
            ## CREACION DEL CARRITO
            ##
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
        es_superu = None
        try:
            usuario = Usuario.objects.get(correo=correo)
        except:
            es_superu = True

        if u_auth is not None:
            login(request, u_auth)
            if es_superu:
                return redirect('admin:index')
            else:
                if (usuario.fk_id_rol_id == 1):
                    return redirect('index_admin')
                elif (usuario.fk_id_rol_id == 2):
                    return redirect('index_admin')
                elif (usuario.fk_id_rol_id == 3):
                    return redirect('index_admin')
                elif (usuario.fk_id_rol_id == 4):
                    return redirect('index_admin')
                elif (usuario.fk_id_rol_id == 5):
                    return redirect('perfil')
        else:
            messages.success(
                request, 'El correo o la contraseña son incorrectos.')
            return redirect('iniciar_sesion')
    else:
        return render(request, 'login.html')
# Para hacer que solo pueda ingresar si es que esta logeado
# @login_required


def cerrar_sesion(request):
    logout(request)
    return redirect('iniciar_sesion')


# Nuevo producto
def newProd(request):
    nombre = request.POST['nomprod']
    stock = request.POST['stockprod']
    desc = request.POST['descprod']
    prove = request.POST['proveedor']
    imagen = request.FILES['imgprod']
    precio = request.POST['precioprod']

    proveedor = Proveedor.objects.get(id_proveedor=prove)

    Producto.objects.create(nombre_producto=nombre, stock=stock,
                            precio=precio, descripcion=desc,imagenProd = imagen,fk_id_proveedor_id=prove)
    return redirect('index_admin')



# Modificar Producto
@login_required(login_url="iniciar_sesion/")
def modificarProducto(request, idProd):
    if request.method == "POST":
        producto = Producto.objects.get(id_producto=idProd)
        provee = request.POST['proveedor']
        proveedor = Proveedor.objects.get(id_proveedor=provee)
        producto.nombre_producto = request.POST.get('nomprod')
        producto.stock = request.POST.get('stockprod')
        producto.precio = request.POST.get('precioprod')
        producto.descripcion = request.POST.get('descprod')
        producto.fk_id_proveedor = proveedor
        if (request.FILES.get("imgprod")):
            fotoprod =  request.FILES['imgprod']
            producto.imagenProd = fotoprod
        producto.save()
        messages.success(request, '¡Producto Modificado!')
        return redirect('index_admin')

    else:
        productoM = Producto.objects.get(id_producto=idProd)
        proveedores = Proveedor.objects.all()
        return render(request, 'modificar.html', {'producto': productoM, 'proveedor_m': proveedores})


def eliminarProducto(request, idProd):
    producto = Producto.objects.get(id_producto=idProd)
    producto.delete()

    messages.success(request, '¡Producto Eliminado!')

    return redirect('index_admin')


"""
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
    
"""
def agregar_producto(request, id_prod):
    if request.user.is_authenticated:
        usuario = request.user
        productos = Producto.objects.get(id_producto=id_prod)
        carrito = Carrito.objects.create(fk_id_usuario=usuario,total = productos.precio,fk_id_producto = productos)
        return redirect('carrito')
    else:
        return redirect('login')

def eliminar_producto(request, id_producto):
    if request.user.is_authenticated:
        producto = Producto.objects.get(id=id_producto)
        carrito = Carrito.objects.get(usuario=request.user)
        carrito.productos.remove(producto)
        carrito.save()
        return redirect('carrito')
    else:
        return redirect('login')