from datetime import datetime 
import requests
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import JsonResponse
from .Carrito import Carrito
from .models import Comuna, Pedido, Producto, Proveedor, ReciboPedido, Rol, Usuario, Solicitud
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db.models import Q



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
    producto = Producto.objects.filter(fk_id_proveedor=1, prod_is_active=1)[:3]
    usuario = Usuario.objects.filter(correo=request.user.username).first()
    contexto = {'producto': producto, 'usuario': usuario}
    rol_admin = None
    try:
        rol = usuario.fk_id_rol_id
        rol_admin = True
    except:
        rol_admin = False

    if rol_admin:
        return render(request, 'index_admin.html')
    else:
        return render(request, 'index.html', contexto)


@login_required(login_url="iniciar_sesion/")
# @role_required('1')
# @role_required('2')
# @role_required('3')
# @role_required('4')
def index_admin(request):
    usuarios = Usuario.objects.filter(correo=request.user.username).first()
    roles = Rol.objects.all()
    return render(request, 'index_admin.html', {'usuarios': usuarios, 'roles': roles})


def agregarProd(request):
    proveedores = Proveedor.objects.all()
    contexto = {'proveedor_m': proveedores}

    return render(request, 'agregarProd.html', contexto)
# Index de modificar o eliminar producto


@login_required(login_url="iniciar_sesion/")
def productos(request):
    return render(request, 'productos.html')


@login_required(login_url="iniciar_sesion/")
def proveedores(request):

    return render(request, 'proveedores.html')


# Pagina de stock de productos
@login_required(login_url="iniciar_sesion/")
def stock_productos(request):
    producto = Producto.objects.filter(row_status=1)
    contexto = {'producto': producto}
    return render(request, 'stock_productos.html', contexto)

# Solicitar stock a proveedores


@login_required(login_url="iniciar_sesion/")
def solicitar_stock(request, id_prod):
    producto = Producto.objects.get(id_producto=id_prod)
    if request.method == "POST":
        usuario = Usuario.objects.filter(correo=request.user.username).first()
        cantidad = request.POST['cantidad']
        Solicitud.objects.create(cantidad_solicitud=cantidad, estado="pendiente", realizado_por=usuario.correo,
                                 fk_id_proveedor=producto.fk_id_proveedor, fk_id_producto_id=id_prod)
        producto.save()
        return redirect('stock_productos')
    else:
        contexto = {'producto': producto}
        return render(request, 'solicitar_stock.html', contexto)

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
        return render(request, 'modificar.html', {'producto': productoM, 'proveedores': proveedores})


def catalogo(request):
    producto = Producto.objects.filter(fk_id_proveedor=1, prod_is_active=1)

    contexto = {'producto': producto}

    return render(request, 'catalogo.html', contexto)


def iniciar_session(request):

    return render(request, 'login.html')


def carrito(request):
    if request.user.is_authenticated:

        return render(request, 'carrito.html')
    else:
        return redirect('login')


def editarperfil(request):
    usuario = Usuario.objects.filter(correo=request.user.username).first()
    contexto = {'usuario': usuario}
    return render(request, 'editarperfil.html', contexto)


@login_required(login_url="iniciar_sesion/")
def modificarPerfil(request, id_usuario):
    if request.method == "POST":
        usuario = Usuario.objects.get(id_usuario=id_usuario)
        usuario.nombre_usuario = request.POST.get('nomusu')
        usuario.apellido_usuario = request.POST.get('apellidousu')
        usuario.celular = request.POST.get('celularusu')
        usuario.direccion = request.POST.get('direccionusu')
        usuario.save()
        contexto = {'usuario': usuario}
        messages.success(request, '¡Información modificada!')
        return render(request, 'perfil.html', contexto)
    else:
        usuarioM = Usuario.objects.get(id_usuario=id_usuario)
    return render(request, 'editarperfil.html', {'usuario': usuarioM})


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
            # CREACION DEL CARRITO
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
                # admin
                if (usuario.fk_id_rol_id == 1):
                    return redirect('index_admin')
                # jefe de local
                elif (usuario.fk_id_rol_id == 2):
                    return redirect('index_admin')
                # cocinero
                elif (usuario.fk_id_rol_id == 3):
                    return redirect('index_admin')
                # vendedor
                elif (usuario.fk_id_rol_id == 4):
                    return redirect('index_admin')
                # cliente
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
                            precio=precio, descripcion=desc, imagenProd=imagen, fk_id_proveedor_id=prove)
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
            fotoprod = request.FILES['imgprod']
            producto.imagenProd = fotoprod
        producto.save()
        messages.success(request, '¡Producto Modificado!')
        return redirect('index_admin')
    else:
        productoM = Producto.objects.get(id_producto=idProd)
        proveedores = Proveedor.objects.all()
        return render(request, 'modificar.html', {'producto': productoM, 'proveedor': proveedores})


@login_required(login_url="iniciar_sesion/")
def agregar_prov(request):
    if request.method == "POST":
        nombre_proveedor = request.POST['nom_prov']
        rut_proveedor = request.POST['rut_prov']
        direccion_proveedor = request.POST['dir_prov']
        descripcion_proveedor = request.POST['desc_prov']
        Proveedor.objects.create(nombre_proveedor=nombre_proveedor, descripcion=descripcion_proveedor,
                                 rut_proveedor=rut_proveedor, direccion=direccion_proveedor, prov_is_active=True, row_status=True)
        return redirect('proveedores')
    else:
        productos = Producto.objects.all()
        contexto = {'productos': productos}
        return render(request, 'agregar_prov.html', contexto)


@login_required(login_url="iniciar_sesion/")
def solicitudes_proveedor(request):
    solicitudes = Solicitud.objects.all()
    contexto = {'solicitudes': solicitudes}
    return render(request, 'solicitudes_proveedor.html', contexto)




def usuarios(request):

    return render(request, 'usuarios.html')

#
# WEBPAY
#


def webpay(request):
    return render(request, 'webpay.html')


def create(request):
    return render(request, 'webpay/plus/create.html')


def commit(request):
    return render(request, 'webpay/plus/commit.html')


def refund(request):
    return render(request, 'webpay/plus/refund-form.html')


def refundform(request):
    return render(request, 'webpay/plus/refund.html')
# VIEWS MODALES
#
#
# URLS
#
#


def sp_lista_solicitudes(request):
    solicitudes = Solicitud.objects.filter(estado="pendiente")
    contexto = {'solicitudes': solicitudes}
    return render(request, 'modales/lista_solicitudes.html', contexto)


def u_lista_usuarios(request):
    usuarios = Usuario.objects.filter(Q(fk_id_rol_id=2) | Q(fk_id_rol_id=3) | Q(
        fk_id_rol_id=4) | Q(fk_id_rol_id=5) & Q(row_status=1))
    roles = Rol.objects.all()
    return render(request, 'modales/lista_usuarios.html', {'usuarios': usuarios, 'roles': roles})


def p_lista_proveedores(request):
    provee = Proveedor.objects.filter(row_status=1)
    contexto = {'proveedor': provee}
    return render(request, 'modales/lista_proveedores.html', contexto)


def sp_finalizar_solicitud(request, id_solicitud):
    solicitud = Solicitud.objects.filter(id_solicitud=id_solicitud).first()
    contexto = {'solicitud': solicitud}
    return render(request, 'modales/sp_finalizar_solicitud.html', contexto)


@login_required(login_url="iniciar_sesion/")
def sp_mas_info(request, id_solicitud):
    solicitudes = Solicitud.objects.get(id_solicitud=id_solicitud)
    return render(request, 'modales/sp_mas_info.html', {'solicitud': solicitudes})


@login_required(login_url="iniciar_sesion/")
def ua_mod_rol(request, id_usuario):
    usuario = Usuario.objects.filter(id_usuario=id_usuario).first()
    roles = Rol.objects.all()

    return render(request, 'modales/ua_mod_rol.html', {'usuario': usuario, 'roles': roles})


@login_required(login_url="iniciar_sesion/")
def ua_eliminar_usuario(request, id_usuario):
    usuario = Usuario.objects.filter(id_usuario=id_usuario).first()

    return render(request, 'modales/ua_eliminar_usuario.html', {'usuario': usuario})


@login_required(login_url="iniciar_sesion/")
def ua_desactivar_usuario(request, id_usuario):
    usuario = Usuario.objects.filter(id_usuario=id_usuario).first()

    return render(request, 'modales/ua_desactivar_usuario.html', {'usuario': usuario})


def ua_activar_usuario(request, id_usuario):
    usuario = Usuario.objects.filter(id_usuario=id_usuario).first()

    return render(request, 'modales/ua_activar_usuario.html', {'usuario': usuario})


def pv_desactivar_proveedor(request, id_proveedor):
    provee = Proveedor.objects.filter(id_proveedor=id_proveedor).first()

    return render(request, 'modales/pv_desactivar_prove.html', {'proveedor': provee})


def pv_activar_proveedor(request, id_proveedor):
    provee = Proveedor.objects.filter(id_proveedor=id_proveedor).first()

    return render(request, 'modales/pv_activar_prove.html', {'proveedor': provee})


def pv_eliminar_proveedor(request, id_proveedor):
    provee = Proveedor.objects.filter(id_proveedor=id_proveedor).first()

    return render(request, 'modales/pv_eliminar_prove.html', {'proveedor': provee})


def p_lista_productos(request):
    producto = Producto.objects.filter(row_status=1)

    return render(request, 'modales/lista_productos.html', {'producto': producto})


def p_activar_producto(request, id_producto):
    producto = Producto.objects.filter(id_producto=id_producto).first()

    return render(request, 'modales/p_activar_producto.html', {'producto': producto})


def p_desactivar_producto(request, id_producto):
    producto = Producto.objects.filter(id_producto=id_producto).first()

    return render(request, 'modales/p_desactivar_producto.html', {'producto': producto})


def p_eliminar_producto(request, id_producto):
    producto = Producto.objects.filter(id_producto=id_producto).first()

    return render(request, 'modales/p_eliminar_producto.html', {'producto': producto})
#
#
# FUNCIONES
#
#


def desactivar_proveedor(request, id_proveedor):
    provee = Proveedor.objects.filter(id_proveedor=id_proveedor).first()
    provee.prov_is_active = False
    provee.save()
    return HttpResponse(status=204, headers={'HX-Trigger': 'actualizar'})


def activar_proveedor(request, id_proveedor):
    provee = Proveedor.objects.filter(id_proveedor=id_proveedor).first()
    provee.prov_is_active = True
    provee.save()
    return HttpResponse(status=204, headers={'HX-Trigger': 'actualizar'})


def eliminar_proveedor(request, id_proveedor):
    provee = Proveedor.objects.filter(id_proveedor=id_proveedor).first()
    provee.row_status = False
    provee.save()
    return HttpResponse(status=204, headers={'HX-Trigger': 'actualizar'})

# Funcion para desactivar al usuario


def desactivar_usuario(request, id_usuario):
    usuario = Usuario.objects.filter(id_usuario=id_usuario).first()
    usuario.u_is_active = False
    usuario.save()
    return HttpResponse(status=204, headers={'HX-Trigger': 'actualizacion'})
# Funcion para activar al usuario


def activar_usuario(request, id_usuario):
    usuario = Usuario.objects.filter(id_usuario=id_usuario).first()
    usuario.u_is_active = True
    usuario.save()
    return HttpResponse(status=204, headers={'HX-Trigger': 'actualizacion'})

# Funcion para eliminar usuario


def eliminar_usuario(request, id_usuario):
    usuario = Usuario.objects.filter(id_usuario=id_usuario).first()
    usuario.row_status = False
    usuario.save()
    return HttpResponse(status=204, headers={'HX-Trigger': 'actualizacion'})


def modificarRol(request, id_usuario):
    if request.method == "POST":
        rol = request.POST['roles']
        usuario = Usuario.objects.filter(id_usuario=id_usuario).first()
        rol = Rol.objects.get(id_rol=rol)
        usuario.fk_id_rol_id = rol.id_rol
        usuario.save()
        return HttpResponse(status=204, headers={'HX-Trigger': 'actualizacion'})


def finalizar_solicitud(request, id_solicitud):
    solicitud = Solicitud.objects.filter(id_solicitud=id_solicitud).first()
    solicitud.estado = "finalizado"
    producto = Producto.objects.filter(
        id_producto=solicitud.fk_id_producto_id).first()
    # producto.stock + solicitud.cantidad_solicitudz

    solicitud.save()
    return HttpResponse(status=204, headers={'HX-Trigger': 'act'})

def activar_producto(request, id_producto):
    producto = Producto.objects.filter(id_producto=id_producto).first()
    producto.prod_is_active = True
    producto.save()
    return HttpResponse(status=204, headers={'HX-Trigger': 'actualizar'})


def desactivar_producto(request, id_producto):
    producto = Producto.objects.filter(id_producto=id_producto).first()
    producto.prod_is_active = False
    producto.save()
    return HttpResponse(status=204, headers={'HX-Trigger': 'actualizar'})


def eliminar_producto(request, id_producto):
    producto = Producto.objects.filter(id_producto=id_producto).first()
    producto.row_status = False
    producto.save()
    return HttpResponse(status=204, headers={'HX-Trigger': 'actualizar'})

####FUNCIONES CARRITO



def agregar_producto(request, idProducto):
    carrito = Carrito(request)
    producto = Producto.objects.get(id_producto = idProducto)
    carrito.agregar(producto)
    return redirect("carrito")

def eliminar_prod_cart(request, idProducto):
    carrito = Carrito(request)
    producto = Producto.objects.get(id_producto = idProducto)
    carrito.eliminar(producto)
    return redirect("carrito")

def restar_producto(request, idProducto):
    carrito = Carrito(request)
    producto = Producto.objects.get(id_producto = idProducto)
    carrito.restar(producto)
    return redirect("carrito")

def limpiar_carrito(request):
    carrito = Carrito(request)
    carrito.limpiar()
    return redirect("carrito")

def obtener_fecha_actual():
    respuesta = requests.get('http://worldtimeapi.org/api/timezone/Etc/UTC')
    data = respuesta.json()
    fecha_actual = datetime.fromisoformat(data['datetime'])
    return fecha_actual

def guardarPedido(request,total):
    usuario = Usuario.objects.filter(correo=request.user.username).first()
    direccion_desc = 'Hacia la dirección ' + usuario.direccion
    fecha_actual = obtener_fecha_actual().date()
    # Crear un nuevo pedido
    pedido = Pedido.objects.create(descripcion=direccion_desc, fecha=fecha_actual, fk_id_usuario_id=usuario.id_usuario,total = total)
    # Crear un nuevo recibo de pedido asociado al pedido y usuario
    recibo_pedido = ReciboPedido.objects.create(estado_pedido='En proceso', fk_id_pedido=pedido, fk_id_usuario=usuario)
    # Obtener los IDs de los productos en el carrito
    ids_productos = request.session.carrito.items.values_list('producto_id', flat=True)
    # Agregar los productos al recibo de pedido
    recibo_pedido.fk_id_productos.add(ids_productos)
    
    return redirect("carrito")


def verPedido(request):
    usuario = Usuario.objects.filter(correo=request.user.username).first()
    pedido = Pedido.objects.get(fk_id_usuario_id = usuario.id_usuario )
    detalle =ReciboPedido.objects.get(fk_id_pedido_id = pedido.id_pedido)
    return render (request,'seguimiento.html',{'pedido':pedido,'detalle':detalle})