from django import forms
from .models import Producto, Proveedor,Comuna,Usuario,Rol
from django.contrib.auth.models import User
from django.forms import ValidationError
import re
from rut_chile import rut_chile

class producto_form(forms.ModelForm):
    stock= forms.IntegerField()
    precio=forms.IntegerField()
    imagen_producto= forms.ImageField()
    class Meta:
        model= Producto
        fields=['nombre_producto','stock','precio','imagen_producto','descripcion','fk_id_proveedor']
        labels={
            'nombre_producto': 'Nombre del producto',
            'imagen_producto': 'Imagen',
            'descripcion': 'Descripción',
            'fk_id_proveedor': 'Proveedor'
        }
        widgets={
            'descripcion': forms.Textarea(attrs={
                "rows":5
            }),
        }
    def clean(self):
        cleaned_data = super().clean()
        stock = cleaned_data.get("stock")
        precio = cleaned_data.get("precio")

        if stock is None or stock <= 0:
            raise forms.ValidationError('El stock debe ser mayor a 1.')
        if precio is None or precio <= 499:
            raise forms.ValidationError('El precio debe ser $500 o mayor.')

        return cleaned_data

class proveedor_form(forms.ModelForm):
    rut_proveedor=forms.CharField(help_text='Debe escribir el RUT con guión.<br>Ejemplo:19283923-1')
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
    def clean(self):
        cleaned_data = super().clean()
        rut_proveedor = cleaned_data.get("rut_proveedor")
        if not rut_chile.is_valid_rut(rut_proveedor):
            raise forms.ValidationError('El rut ingresado no es válido.')

        return cleaned_data
class registrar_usuario_form(forms.Form):
    nombre_usuario=forms.CharField(label="Nombre",widget=forms.TextInput(attrs={'class': 'col-6'}))
    apellido_usuario=forms.CharField(label="Apellido",widget=forms.TextInput(attrs={'class': 'col-6'}))
    correo=forms.EmailField(label="Correo electrónico")
    direccion=forms.CharField(label="Dirección")
    comuna=forms.ModelChoiceField(queryset=Comuna.objects.all(),label="Comuna")
    celular=forms.IntegerField(label="Celular", help_text="El número debe comenzar con 9.<br>Ejemplo: 912345678")
    clave=forms.CharField(widget=forms.PasswordInput,label="Contraseña",help_text="<strong><p id='show-hide' onclick='togglePassword()' style='cursor:pointer;' >Mostrar contraseña</p></strong>La contraseña debe contener:<br>Al menos 8 caracteres.<br>Una letra meyúscula.<br>Un caracter especial.")
    confirmar_clave=forms.CharField(widget=forms.PasswordInput,label="Confirmar contraseña")
    def clean_cel(self):
        cel= self.cleaned_data['celular']
        # Se transforma a string ya que las validaciones no funcionan si este dato es int.
        celular= str(cel)
        if len(celular) != 9:
            raise forms.ValidationError('El celular ingresado no es válido.')
        if not celular.startswith("9"):
            raise forms.ValidationError('El número debe comenzar con 9.')
        return celular
    def clean_email(self):
        correo= self.cleaned_data['correo']
        if User.objects.filter(username__iexact=correo).exists():
            raise forms.ValidationError('El correo ingresado ya posee una cuenta asociada.')
        if re.match("^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", correo) is None:
            raise forms.ValidationError('Ingrese un correo válido.')
        return correo
    def clean_password(self):
        clave= self.cleaned_data['clave']
        confirmar_clave= self.cleaned_data['confirmar_clave']
        if clave != confirmar_clave:
            raise forms.ValidationError('Las contraseñas ingresadas no coinciden.')
        if len(clave) < 8:
            raise forms.ValidationError('La contraseña debe tener, como mínimo, 8 caracteres.')
        if not re.search("[A-Z]", clave):
            raise forms.ValidationError('La contraseña debe tener una letra mayúscula.')
        if not re.search("[!@#$%^&*()_+-={};:'\"|,.<>/?]", clave):
            raise forms.ValidationError('La contraseña debe tener un caracter especial (!,@,*,etc...)')
        return clave
    def clean(self):
        cleaned_data = super().clean()
        correo = cleaned_data.get("correo")
        clave = cleaned_data.get("clave")
        celular = cleaned_data.get("celular")
        # Add your validation here
        self.clean_email()
        self.clean_password()
        self.clean_cel()
        return cleaned_data

#FORMULARIOS DEL USUARIO QUE SERÁN EXCLUSIVAMENTE DEL ADMINISTRADOR
class usuario_form(forms.Form):
    nombre_usuario=forms.CharField(label="Nombre",widget=forms.TextInput(attrs={'class': 'col-6'}))
    apellido_usuario=forms.CharField(label="Apellido",widget=forms.TextInput(attrs={'class': 'col-6'}))
    correo=forms.EmailField(label="Correo electrónico")
    direccion=forms.CharField(label="Dirección")
    comuna=forms.ModelChoiceField(queryset=Comuna.objects.all(),label="Comuna")
    celular=forms.IntegerField(label="Celular", help_text="El número debe comenzar con 9.<br>Ejemplo: 912345678")
    clave=forms.CharField(widget=forms.PasswordInput,label="Contraseña",help_text="<strong><p id='show-hide' onclick='togglePassword()' style='cursor:pointer;' >Mostrar contraseña</p></strong>La contraseña debe contener:<br>Al menos 8 caracteres.<br>Una letra meyúscula.<br>Un caracter especial.")
    confirmar_clave=forms.CharField(widget=forms.PasswordInput,label="Confirmar contraseña")
    rol=forms.ModelChoiceField(queryset=Rol.objects.all(),label="Rol")
    def clean_cel(self):
        cel= self.cleaned_data['celular']
        # Se transforma a string ya que las validaciones no funcionan si este dato es int.
        celular= str(cel)
        if len(celular) != 9:
            raise forms.ValidationError('El celular ingresado no es válido.')
        if not celular.startswith("9"):
            raise forms.ValidationError('El número debe comenzar con 9.')
        return celular
    def clean_email(self):
        correo= self.cleaned_data['correo']
        if User.objects.filter(username__iexact=correo).exists():
            raise forms.ValidationError('El correo ingresado ya posee una cuenta asociada.')
        if re.match("^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", correo) is None:
            raise forms.ValidationError('Ingrese un correo válido.')
        return correo
    def clean_password(self):
        clave= self.cleaned_data['clave']
        confirmar_clave= self.cleaned_data['confirmar_clave']
        if clave != confirmar_clave:
            raise forms.ValidationError('Las contraseñas ingresadas no coinciden.')
        if len(clave) < 8:
            raise forms.ValidationError('La contraseña debe tener, como mínimo, 8 caracteres.')
        if not re.search("[A-Z]", clave):
            raise forms.ValidationError('La contraseña debe tener una letra mayúscula.')
        if not re.search("[!@#$%^&*()_+-={};:'\"|,.<>/?]", clave):
            raise forms.ValidationError('La contraseña debe tener un caracter especial (!,@,*,etc...)')
        return clave
    def clean(self):
        cleaned_data = super().clean()
        correo = cleaned_data.get("correo")
        clave = cleaned_data.get("clave")
        celular = cleaned_data.get("celular")
        # Add your validation here
        self.clean_email()
        self.clean_password()
        self.clean_cel()
        return cleaned_data
class modificar_usuario_form(forms.ModelForm):
    class Meta:
        model=Usuario
        fields=['nombre_usuario','apellido_usuario','correo','direccion','fk_id_comuna','celular']
        labels={
            'nombre_usuario':'Nombre',
            'apellido_usuario':'Apellido',
            'correo':'Correo electrónico',
            'direccion':'Dirección',
            'fk_id_comuna':'Comuna',
            'celular':'Celular'
        }