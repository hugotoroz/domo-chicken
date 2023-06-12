from datetime import datetime 
import requests
from django.contrib import messages
from django.http import HttpResponse,Http404
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import JsonResponse
from .Carrito import Carrito
from .models import Comuna, Pedido, Producto, Proveedor, ReciboPedido, Rol, Usuario, Solicitud
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.auth.models import User
from .forms import producto_form, proveedor_form, usuario_form,modificar_usuario_form,registrar_usuario_form
from django.db.models import Q

#ERRORES
def pagina_no_encontrada(request, exception):
    return render(request, 'handlers/404.html', status=404)
def error_servidor(request):
    return render(request, 'handlers/500.html', status=500)

def check_role(role):
    def test(user):
        return user.is_authenticated and Usuario.objects.filter(fk_id_rol=role, correo=user.username).exists()
    return test
def role_required(*role):
    def decorator(view_func):
        decorated_view_func = user_passes_test(check_role(role), login_url="/", redirect_field_name=None)(view_func)
        def wrapper(request, *args, **kwargs):
            if check_role(role)(request.user):
                return decorated_view_func(request, *args, **kwargs)
            else:
                raise Http404
        return wrapper
    return decorator

def index(request):
    producto = Producto.objects.filter(fk_id_proveedor=1, prod_is_active=1)[:3]
    usuario = Usuario.objects.filter(correo=request.user.username).first()
    contexto = {'producto': producto, 'usuario': usuario}
    rol = None
    try:
        rol = usuario.fk_id_rol_id
    except:
        rol=5

    if rol==1:
        return redirect('index_admin')
    else:
        return render(request, 'index.html', contexto)


@login_required(login_url="/")
@role_required('1')
def index_admin(request):
    usuarios = Usuario.objects.filter(correo=request.user.username).first()
    roles = Rol.objects.all()
    return render(request, 'index_admin.html', {'usuarios': usuarios, 'roles': roles})

@login_required(login_url="/")
@role_required('1','2')
def agregar_producto_nuevo(request):
    if request.method == "POST":
        form_agregar_producto = producto_form(
            request.POST, request.FILES)
        if form_agregar_producto.is_valid():
            form_agregar_producto.save()
            return redirect('productos')
    else:
        form_agregar_producto = producto_form()
        contexto = {'form': form_agregar_producto}
        return render(request, 'agregar_producto.html', contexto)

@login_required(login_url="/")
@role_required('1','4')
def productos(request):
    return render(request, 'productos.html')

@login_required(login_url="/")
@role_required('1','4')
def proveedores(request):
    return render(request, 'proveedores.html')


# Pagina de stock de productos
@login_required(login_url="/")
@role_required('1','4')
def stock_productos(request):
    producto = Producto.objects.filter(row_status=1)
    contexto = {'producto': producto}
    return render(request, 'stock_productos.html', contexto)

# Solicitar stock a proveedores


@login_required(login_url="/")
@role_required('1','4')
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

@login_required(login_url="/")
@role_required('1')
def modificar_producto(request, idProd):
    producto_filter = Producto.objects.get(id_producto=idProd)
    if request.method == "POST":
        form_agregar_producto = producto_form(
            request.POST, request.FILES, instance=producto_filter)
        if form_agregar_producto.is_valid():
            form_agregar_producto.save()
            return redirect('productos')
    else:
        form_agregar_producto = producto_form(instance=producto_filter)
        contexto = {'producto': producto_filter, 'form': form_agregar_producto}
        return render(request, 'modificar.html', contexto)


def catalogo(request):
    producto = Producto.objects.filter(fk_id_proveedor=1, prod_is_active=1)
    contexto = {'producto': producto}
    return render(request, 'catalogo.html', contexto)

def carrito(request):
    if request.user.is_authenticated:

        return render(request, 'carrito.html')
    else:
        return redirect('login')


def editarperfil(request):
    usuario = Usuario.objects.filter(correo=request.user.username).first()
    contexto = {'usuario': usuario}
    return render(request, 'editarperfil.html', contexto)


@login_required(login_url="/")
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


@login_required(login_url="/")
def perfil(request):
    usuario = Usuario.objects.filter(correo=request.user.username).first()
    contexto = {'usuario': usuario}
    return render(request, 'perfil.html', contexto)

# Registro de usuarios.


def registrar_usuario(request):
    if request.method == "POST":
        form_registrar_usuario = registrar_usuario_form(request.POST)
        if form_registrar_usuario.is_valid():
            nombre_usuario = request.POST['nombre_usuario']
            apellido_usuario = request.POST['apellido_usuario']
            correo = request.POST['correo']
            clave = request.POST['clave']
            comuna = request.POST['comuna']
            direccion = request.POST['direccion']
            celular = request.POST['celular']

            User.objects.create_user(correo, '', clave)
            Usuario.objects.create(nombre_usuario=nombre_usuario, apellido_usuario=apellido_usuario,correo=correo,  direccion=direccion,fk_id_comuna_id=comuna,celular=celular)
            u_auth = authenticate(request, username=correo, password=clave)
            login(request, u_auth)
            
            #form_agregar_usuario.save()
            return redirect('index')
    else:
        form_registrar_usuario = registrar_usuario_form()
        contexto = {'form': form_registrar_usuario}
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
            is_act= usuario.u_is_active
        except:
            es_superu = True

        if u_auth is not None and is_act==1 :
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


def cerrar_sesion(request):
    logout(request)
    return redirect('iniciar_sesion')


def agregar_prov(request):
    if request.method == "POST":
        form_agregar_proveedor = proveedor_form(request.POST)
        if form_agregar_proveedor.is_valid():
            form_agregar_proveedor.save()
            return redirect('proveedores')
    else:
        form_agregar_proveedor = proveedor_form()
        contexto = {'form': form_agregar_proveedor}
        return render(request, 'agregar_prov.html', contexto)


@login_required(login_url="/")
def modificar_proveedor(request, id_prov):
    prov_filter = Proveedor.objects.get(id_proveedor=id_prov)
    if request.method == "POST":
        form_agregar_proveedor = proveedor_form(
            request.POST, instance=prov_filter)
        if form_agregar_proveedor.is_valid():
            form_agregar_proveedor.save()
            return redirect('proveedores')
    else:
        form_agregar_proveedor = proveedor_form(instance=prov_filter)
        contexto = {'form': form_agregar_proveedor}
        return render(request, 'modificar_prov.html', contexto)


@login_required(login_url="/")
def solicitudes_proveedor(request):
    solicitudes = Solicitud.objects.all()
    contexto = {'solicitudes': solicitudes}
    return render(request, 'solicitudes_proveedor.html', contexto)

def usuarios(request):

    return render(request, 'usuarios.html')

@login_required(login_url="/")
@role_required('1')
def agregar_usuario(request):
    if request.method == "POST":
        form_agregar_usuario = usuario_form(request.POST)
        if form_agregar_usuario.is_valid():
            nombre_usuario = request.POST['nombre_usuario']
            apellido_usuario = request.POST['apellido_usuario']
            correo = request.POST['correo']
            clave = request.POST['clave']
            comuna = request.POST['comuna']
            direccion = request.POST['direccion']
            celular = request.POST['celular']
            rol = request.POST['rol']

            User.objects.create_user(correo, '', clave)
            Usuario.objects.create(nombre_usuario=nombre_usuario, apellido_usuario=apellido_usuario,correo=correo,  direccion=direccion,fk_id_comuna_id=comuna,celular=celular,fk_id_rol_id=rol)
            #form_agregar_usuario.save()
            return redirect('usuarios')
    else:
        form_agregar_usuario = usuario_form()
        contexto = {'form': form_agregar_usuario}
        return render(request, 'agregar_usuario.html', contexto)

@login_required(login_url="/")
@role_required('1')
def modificar_usuario(request, id_user):
    usuario_filter = Usuario.objects.get(id_usuario=id_user)
    if request.method == "POST":
        form_modificar_usuario = modificar_usuario_form(request.POST, instance=usuario_filter)
        if form_modificar_usuario.is_valid():
            form_modificar_usuario.save()
            return redirect('usuarios')
    else:
        form_modificar_usuario = modificar_usuario_form(instance=usuario_filter)
        contexto = {'form': form_modificar_usuario}
        return render(request, 'modificar_usuario.html', contexto)
@login_required(login_url="/")
@role_required('1','3')
def index_repartidor(request):
    pedidos = Pedido.objects.all()
    contexto = {'pedidos': pedidos}
    return render(request, 'index_repartidor.html', contexto)


#
# COCINERO 
#

def index_cocinero(request):
    solicitudes = Solicitud.objects.filter(estado="pendiente")
    contexto = {'solicitudes': solicitudes}
    return render(request, 'index_cocinero.html', contexto)



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

@login_required(login_url="/")
@role_required('1','4')
def sp_lista_solicitudes(request):
    solicitudes = Solicitud.objects.filter(estado="pendiente")
    contexto = {'solicitudes': solicitudes}
    return render(request, 'modales/lista_solicitudes.html', contexto)

@login_required(login_url="/")
@role_required('1')
def u_lista_usuarios(request):
    usuarios = Usuario.objects.filter(Q(fk_id_rol_id=2) | Q(fk_id_rol_id=3) | Q(
        fk_id_rol_id=4) | Q(fk_id_rol_id=5) & Q(row_status=1))
    roles = Rol.objects.all()
    return render(request, 'modales/lista_usuarios.html', {'usuarios': usuarios, 'roles': roles})

@login_required(login_url="/")
@role_required('1','4')
def p_lista_proveedores(request):
    provee = Proveedor.objects.filter(row_status=1)
    contexto = {'proveedor': provee}
    return render(request, 'modales/lista_proveedores.html', contexto)

@login_required(login_url="/")
@role_required('1','4')
def sp_finalizar_solicitud(request, id_solicitud):
    solicitud = Solicitud.objects.filter(id_solicitud=id_solicitud).first()
    contexto = {'solicitud': solicitud}
    return render(request, 'modales/sp_finalizar_solicitud.html', contexto)


@login_required(login_url="/")
@role_required('1','4')
def sp_mas_info(request, id_solicitud):
    solicitudes = Solicitud.objects.get(id_solicitud=id_solicitud)
    return render(request, 'modales/sp_mas_info.html', {'solicitud': solicitudes})


@login_required(login_url="/")
@role_required('1')
def ua_mod_rol(request, id_usuario):
    usuario = Usuario.objects.filter(id_usuario=id_usuario).first()
    roles = Rol.objects.all()

    return render(request, 'modales/ua_mod_rol.html', {'usuario': usuario, 'roles': roles})


@login_required(login_url="/")
@role_required('1')
def ua_eliminar_usuario(request, id_usuario):
    usuario = Usuario.objects.filter(id_usuario=id_usuario).first()

    return render(request, 'modales/ua_eliminar_usuario.html', {'usuario': usuario})


@login_required(login_url="/")
@role_required('1')
def ua_desactivar_usuario(request, id_usuario):
    usuario = Usuario.objects.filter(id_usuario=id_usuario).first()

    return render(request, 'modales/ua_desactivar_usuario.html', {'usuario': usuario})

@login_required(login_url="/")
@role_required('1')
def ua_activar_usuario(request, id_usuario):
    usuario = Usuario.objects.filter(id_usuario=id_usuario).first()

    return render(request, 'modales/ua_activar_usuario.html', {'usuario': usuario})

@login_required(login_url="/")
@role_required('1')
def pv_desactivar_proveedor(request, id_proveedor):
    provee = Proveedor.objects.filter(id_proveedor=id_proveedor).first()

    return render(request, 'modales/pv_desactivar_prove.html', {'proveedor': provee})

@login_required(login_url="/")
@role_required('1')
def pv_activar_proveedor(request, id_proveedor):
    provee = Proveedor.objects.filter(id_proveedor=id_proveedor).first()

    return render(request, 'modales/pv_activar_prove.html', {'proveedor': provee})

@login_required(login_url="/")
@role_required('1')
def pv_eliminar_proveedor(request, id_proveedor):
    provee = Proveedor.objects.filter(id_proveedor=id_proveedor).first()

    return render(request, 'modales/pv_eliminar_prove.html', {'proveedor': provee})

@login_required(login_url="/")
@role_required('1','4')
def p_lista_productos(request):
    producto = Producto.objects.filter(row_status=1)

    return render(request, 'modales/lista_productos.html', {'producto': producto})

@login_required(login_url="/")
@role_required('1')
def p_activar_producto(request, id_producto):
    producto = Producto.objects.filter(id_producto=id_producto).first()

    return render(request, 'modales/p_activar_producto.html', {'producto': producto})

@login_required(login_url="/")
@role_required('1')
def p_desactivar_producto(request, id_producto):
    producto = Producto.objects.filter(id_producto=id_producto).first()

    return render(request, 'modales/p_desactivar_producto.html', {'producto': producto})

@login_required(login_url="/")
@role_required('1')
def p_eliminar_producto(request, id_producto):
    producto = Producto.objects.filter(id_producto=id_producto).first()

    return render(request, 'modales/p_eliminar_producto.html', {'producto': producto})
#
#
# FUNCIONES
#
#

@login_required(login_url="/")
@role_required('1')
def desactivar_proveedor(request, id_proveedor):
    provee = Proveedor.objects.filter(id_proveedor=id_proveedor).first()
    provee.prov_is_active = False
    provee.save()
    return HttpResponse(status=204, headers={'HX-Trigger': 'actualizar'})

@login_required(login_url="/")
@role_required('1')
def activar_proveedor(request, id_proveedor):
    provee = Proveedor.objects.filter(id_proveedor=id_proveedor).first()
    provee.prov_is_active = True
    provee.save()
    return HttpResponse(status=204, headers={'HX-Trigger': 'actualizar'})

@login_required(login_url="/")
@role_required('1')
def eliminar_proveedor(request, id_proveedor):
    provee = Proveedor.objects.filter(id_proveedor=id_proveedor).first()
    provee.row_status = False
    provee.save()
    return HttpResponse(status=204, headers={'HX-Trigger': 'actualizar'})

# Funcion para desactivar al usuario

@login_required(login_url="/")
@role_required('1')
def desactivar_usuario(request, id_usuario):
    usuario = Usuario.objects.filter(id_usuario=id_usuario).first()
    usuario.u_is_active = False
    usuario.save()
    return HttpResponse(status=204, headers={'HX-Trigger': 'actualizacion'})
# Funcion para activar al usuario

@login_required(login_url="/")
@role_required('1')
def activar_usuario(request, id_usuario):
    usuario = Usuario.objects.filter(id_usuario=id_usuario).first()
    usuario.u_is_active = True
    usuario.save()
    return HttpResponse(status=204, headers={'HX-Trigger': 'actualizacion'})

# Funcion para eliminar usuario

@login_required(login_url="/")
@role_required('1')
def eliminar_usuario(request, id_usuario):
    usuario = Usuario.objects.filter(id_usuario=id_usuario).first()
    usuario.row_status = False
    usuario.save()
    return HttpResponse(status=204, headers={'HX-Trigger': 'actualizacion'})

@login_required(login_url="/")
@role_required('1')
def modificarRol(request, id_usuario):
    if request.method == "POST":
        rol = request.POST['roles']
        usuario = Usuario.objects.filter(id_usuario=id_usuario).first()
        rol = Rol.objects.get(id_rol=rol)
        usuario.fk_id_rol_id = rol.id_rol
        usuario.save()
        return HttpResponse(status=204, headers={'HX-Trigger': 'actualizacion'})

@login_required(login_url="/")
@role_required('1','4')
def finalizar_solicitud(request, id_solicitud):
    solicitud = Solicitud.objects.filter(id_solicitud=id_solicitud).first()
    solicitud.estado = "finalizado"
    producto = Producto.objects.filter(
        id_producto=solicitud.fk_id_producto_id).first()
    # producto.stock + solicitud.cantidad_solicitudz

    solicitud.save()
    return HttpResponse(status=204, headers={'HX-Trigger': 'act'})

@login_required(login_url="/")
@role_required('1')
def activar_producto(request, id_producto):
    producto = Producto.objects.filter(id_producto=id_producto).first()
    producto.prod_is_active = True
    producto.save()
    return HttpResponse(status=204, headers={'HX-Trigger': 'actualizar'})

@login_required(login_url="/")
@role_required('1')
def desactivar_producto(request, id_producto):
    producto = Producto.objects.filter(id_producto=id_producto).first()
    producto.prod_is_active = False
    producto.save()
    return HttpResponse(status=204, headers={'HX-Trigger': 'actualizar'})

@login_required(login_url="/")
@role_required('1')
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

@login_required(login_url="/")
def guardarPedido(request,total):
    usuario = Usuario.objects.filter(correo=request.user.username).first()
    direccion_desc = 'Hacia la dirección ' + usuario.direccion
    fecha_actual = obtener_fecha_actual().date()
    # Crear un nuevo pedido
    pedido = Pedido.objects.create(descripcion=direccion_desc, fecha=fecha_actual, fk_id_usuario_id=usuario.id_usuario,total = total,estado_pedido='En proceso')
    # Obtener los IDs de los productos en el carrito
    #ids_productos = request.session.carrito.items.values_list('producto_id', flat=True)
    carrito = request.session.get('carrito', {})
    ids_productos = []
    for clave, valor in carrito.items():
        producto_id = valor['producto_id']
        ids_productos.append(producto_id)
    # Crear un nuevo recibo de pedido asociado al pedido y usuario
    recibo_pedido = ReciboPedido.objects.create(fk_id_pedido_id=pedido.id_pedido, fk_id_usuario_id=usuario.id_usuario)
    recibo_pedido.fk_id_productos.add(*ids_productos)
    # Agregar los productos al recibo de pedido
    #recibo_pedido.fk_id_productos.add(ids_productos)
    return redirect("carrito")


def verPedido(request):
    usuario = Usuario.objects.filter(correo=request.user.username).first()
    pedido_usuario = Pedido.objects.filter(fk_id_usuario_id = usuario.id_usuario).values()
    detalle =ReciboPedido.objects.filter(fk_id_usuario_id = usuario.id_usuario).values('fk_id_productos','fk_id_pedido')
    producto =Producto.objects.all()
    print(detalle)    

    return render (request,'seguimiento.html',{'pedido':pedido_usuario,'detalle':detalle,'producto':producto})