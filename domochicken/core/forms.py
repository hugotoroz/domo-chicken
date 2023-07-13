from django import forms
from .models import Producto, Proveedor,Comuna,Usuario,Rol
from django.contrib.auth.models import User
from django.forms import ValidationError
from django.db.models import Q
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
        precio = cleaned_data.get("precio")

        if precio is None or precio <= 499:
            self.add_error('precio','El precio debe ser $500 o mayor.')

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
            self.add_error('rut_proveedor','El rut ingresado no es válido.')

        return cleaned_data
class registrar_usuario_form(forms.Form):
    nombre_usuario=forms.CharField(label="Nombre")
    apellido_usuario=forms.CharField(label="Apellido")
    correo=forms.EmailField(label="Correo electrónico")
    direccion=forms.CharField(label="Dirección")
    comuna=forms.ModelChoiceField(queryset=Comuna.objects.all(),label="Comuna")
    celular=forms.IntegerField(label="Celular", help_text="El número debe comenzar con 9.<br>Ejemplo: 912345678")
    clave=forms.CharField(widget=forms.PasswordInput,label="Contraseña",help_text="<strong><p id='show-hide' onclick='togglePassword()' style='cursor:pointer;' >Mostrar contraseña</p></strong>La contraseña debe contener:<br>Al menos 8 caracteres.<br>Una letra meyúscula.<br>un carácter especial.")
    confirmar_clave=forms.CharField(widget=forms.PasswordInput,label="Confirmar contraseña")
    def clean_cel(self):
        cel= self.cleaned_data['celular']
        # Se transforma a string ya que las validaciones no funcionan si este dato es int.
        celular= str(cel)
        if len(celular) != 9:
            self.add_error('celular','El celular ingresado no es válido.')
        if not celular.startswith("9"):
            self.add_error('celular','El número debe comenzar con 9.')
        return celular
    def clean_email(self):
        correo= self.cleaned_data['correo']
        if User.objects.filter(username__iexact=correo).exists():
            self.add_error('correo','El correo ingresado ya posee una cuenta asociada.')
        if re.match("^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", correo) is None:
            self.add_error('correo','Ingrese un correo válido.')
        return correo
    def clean_password(self):
        clave= self.cleaned_data['clave']
        confirmar_clave= self.cleaned_data['confirmar_clave']
        if clave != confirmar_clave:
            self.add_error('clave','Las contraseñas ingresadas no coinciden.')
        if len(clave) < 8:
            self.add_error('clave','La contraseña debe tener, como mínimo, 8 caracteres.')
        if not re.search("[A-Z]", clave):
            self.add_error('clave','La contraseña debe tener una letra mayúscula.')
        if not re.search("[!@#$%^&*()_+-={};:'\"|,.<>/?]", clave):
            self.add_error('clave','La contraseña debe tener un carácter especial (!,@,*,etc...)')
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
    nombre_usuario=forms.CharField(label="Nombre")
    apellido_usuario=forms.CharField(label="Apellido")
    correo=forms.EmailField(label="Correo electrónico")
    direccion=forms.CharField(label="Dirección")
    comuna=forms.ModelChoiceField(queryset=Comuna.objects.all(),label="Comuna")
    celular=forms.IntegerField(label="Celular", help_text="El número debe comenzar con 9.<br>Ejemplo: 912345678")
    clave=forms.CharField(widget=forms.PasswordInput,label="Contraseña",help_text="<strong><p id='show-hide' onclick='togglePassword()' style='cursor:pointer;' >Mostrar contraseña</p></strong>La contraseña debe contener:<br>Al menos 8 caracteres.<br>Una letra meyúscula.<br>un carácter especial.")
    confirmar_clave=forms.CharField(widget=forms.PasswordInput,label="Confirmar contraseña")
    rol=forms.ModelChoiceField(queryset=Rol.objects.all(),label="Rol")
    def clean_cel(self):
        cel= self.cleaned_data['celular']
        # Se transforma a string ya que las validaciones no funcionan si este dato es int.
        celular= str(cel)
        if len(celular) != 9:
            self.add_error('celular','El celular ingresado no es válido.')
        if not celular.startswith("9"):
            self.add_error('celular','El número debe comenzar con 9.')
        return celular
    def clean_email(self):
        correo= self.cleaned_data['correo']
        if User.objects.filter(username__iexact=correo).exists():
            self.add_error('correo','El correo ingresado ya posee una cuenta asociada.')
        if re.match("^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", correo) is None:
            self.add_error('correo','Ingrese un correo válido.')
        return correo
    def clean_password(self):
        clave= self.cleaned_data['clave']
        confirmar_clave= self.cleaned_data['confirmar_clave']
        if clave != confirmar_clave:
            self.add_error('clave','Las contraseñas ingresadas no coinciden.')
        if len(clave) < 8:
            self.add_error('clave','La contraseña debe tener, como mínimo, 8 caracteres.')
        if not re.search("[A-Z]", clave):
            self.add_error('clave','La contraseña debe tener una letra mayúscula.')
        caracteres_especiales = "!@#$%^&*()_+-={};:'\"|,.<>/?"
        if not any(caracter in caracteres_especiales for caracter in clave):
            self.add_error('clave','La contraseña debe tener al menos un carácter especial (!, @, #, etc...)')
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
    nombre_usuario=forms.CharField(label="Nombre")
    apellido_usuario=forms.CharField(label="Apellido")
    correo=forms.EmailField(label="Correo electrónico")
    direccion=forms.CharField(label="Dirección")
    celular=forms.IntegerField(label="Celular", help_text="El número debe comenzar con 9.<br>Ejemplo: 912345678")
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
    def clean(self):
        cleaned_data = super().clean()
        correo = cleaned_data.get("correo")
        cel = cleaned_data.get("celular")
        celular= str(cel)

        if re.match("^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", correo) is None:
            self.add_error('correo','Ingrese un correo válido.')
        if len(celular) != 9:
            self.add_error('celular','El celular ingresado no es válido.')
        if not celular.startswith("9"):
            self.add_error('celular','El número debe comenzar con 9.')
        return cleaned_data
        

class modificar_clave_form(forms.Form):
    clave=forms.CharField(widget=forms.PasswordInput,label="Nueva contraseña",help_text="<strong><p id='show-hide' onclick='togglePassword()' style='cursor:pointer;' >Mostrar contraseña</p></strong>La contraseña debe contener:<br>Al menos 8 caracteres.<br>Una letra meyúscula.<br>un carácter especial.")
    confirmar_clave=forms.CharField(widget=forms.PasswordInput,label="Confirmar contraseña")
    def clean_password(self):
        clave= self.cleaned_data['clave']
        confirmar_clave= self.cleaned_data['confirmar_clave']
        
        if clave != confirmar_clave:
            raise forms.ValidationError('Las contraseñas ingresadas no coinciden.')
        if len(clave) < 8:
            raise forms.ValidationError('La contraseña debe tener, como mínimo, 8 caracteres.')
        if not re.search("[A-Z]", clave):
            raise forms.ValidationError('La contraseña debe tener una letra mayúscula.')
        caracteres_especiales = "!@#$%^&*()_+-={};:'\"|,.<>/?"
        if not any(caracter in caracteres_especiales for caracter in clave):
            raise forms.ValidationError('La contraseña debe tener al menos un carácter especial (!, @, #, etc...)')
        return clave
    def clean(self):
        cleaned_data = super().clean()
        clave = cleaned_data.get("clave")
        # Add your validation here
        self.clean_password()
        return cleaned_data
    
class solicitar_stock_form(forms.Form):
    cantidad=forms.IntegerField(label="Cantidad a solicitar")
    def clean(self):
        cleaned_data = super().clean()
        cantidad = cleaned_data.get("cantidad")
        
        # Add your validation here
        if cantidad is None or cantidad <= 0:
            self.add_error('cantidad','La cantidad a solicitar debe ser mayor a 1.')
        return cleaned_data
    

class relacionar_producto_form(forms.Form):
    producto=forms.ModelChoiceField(queryset=Producto.objects.exclude(Q(row_status=0) | Q(fk_id_proveedor=1)),label="Seleccione un proveedor", required= False)
    
