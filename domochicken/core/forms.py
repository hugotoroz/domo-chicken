from django import forms
from .models import Producto, Proveedor,Comuna,Usuario,Rol
from django.forms import ValidationError
#VALIDACIONES
class val_largo_numero:
    def __init__(self,largo=9):
        self.largo= largo

    def __call__(self,value):
        ver_largo= len(str(value))
        largo= self.largo
        if ver_largo != largo:
            raise  ValidationError("Ingrese un número válido.")
        return value

class producto_form(forms.ModelForm):
    stock= forms.IntegerField(min_value=1)
    precio=forms.IntegerField(min_value=100)
    imagenProd= forms.ImageField()
    class Meta:
        model= Producto
        fields=['nombre_producto','stock','precio','imagenProd','descripcion','fk_id_proveedor']
        labels={
            'nombre_producto': 'Nombre del producto',
            'imagenProd': 'Imagen',
            'descripcion': 'Descripción',
            'fk_id_proveedor': 'Proveedor'
        }
        widgets={
            'descripcion': forms.Textarea(attrs={
                "rows":5
            }),
        }

class proveedor_form(forms.ModelForm):
    rut_proveedor=forms.CharField(required=False)
    class Meta:
        model=Proveedor
        fields=['nombre_proveedor','rut_proveedor','direccion','descripcion']
        labels={
            'nombre_proveedor': 'Nombre',
            'rut_proveedor': 'Rut (opcional)',
            'direccion': 'Dirección',
            'descripcion' : 'Descripción'
        }
        widgets={
            'descripcion': forms.Textarea(attrs={
                "rows":5
            }),
        }
class registrar_usuario_form(forms.Form):
    nombre_usuario=forms.CharField(label="Nombre")
    apellido_usuario=forms.CharField(label="Apellido")
    correo=forms.EmailField(label="Correo electrónico")
    direccion=forms.CharField(label="Dirección")
    comuna=forms.ModelChoiceField(queryset=Comuna.objects.all(),label="Comuna")
    celular=forms.IntegerField(label="Celular")
    clave=forms.CharField(widget=forms.PasswordInput,label="Contraseña")
    confirmar_clave=forms.CharField(widget=forms.PasswordInput,label="Confirmar contraseña")

#FORMULARIOS DEL USUARIO QUE SERÁN EXCLUSIVAMENTE DEL ADMINISTRADOR
class usuario_form(forms.Form):
    nombre_usuario=forms.CharField(label="Nombre")
    apellido_usuario=forms.CharField(label="Apellido")
    correo=forms.EmailField(label="Correo electrónico")
    direccion=forms.CharField(label="Dirección")
    comuna=forms.ModelChoiceField(queryset=Comuna.objects.all(),label="Comuna")
    celular=forms.IntegerField(label="Celular")
    clave=forms.CharField(widget=forms.PasswordInput,label="Contraseña")
    confirmar_clave=forms.CharField(widget=forms.PasswordInput,label="Confirmar contraseña")
    rol=forms.ModelChoiceField(queryset=Rol.objects.all(),label="Rol")
class modificar_usuario_form(forms.ModelForm):
    class Meta:
        model=Usuario
        fields=['nombre_usuario','apellido_usuario','direccion','fk_id_comuna','celular']
        labels={
            'nombre_usuario':'Nombre',
            'apellido_usuario':'Apellido',
            'direccion':'Dirección',
            'fk_id_comuna':'Comuna',
            'celular':'Celular'
        }