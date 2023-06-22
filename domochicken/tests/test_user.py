import pytest

from core.models import User
from django.test import Client, TestCase

#verificar index
class TemplateTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_template_content(self):
        response = self.client.get('')
        self.assertContains(response, 'Domo Chicken - La mejor calidad')

#verificar catalogo
class TemplateTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_template_content(self):
        response = self.client.get('/catalogo/')
        self.assertContains(response, 'Domo Chicken - La mejor calidad')

#verificar index_cocinero
class TemplateTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_template_content(self):
        response = self.client.get('/index_cocinero')
        self.assertContains(response, 'Domo Chicken - Panel de control de cocinero')

#Verificar si se crean usuarios/prueba unitaria de creación de usuarios
@pytest.mark.django_db
def test_user_creation():
    user = User.objects.create_user(
            username='alexis',
            email='alexis@duocuc.cl',
            password='12345'
    )
    assert user.username == 'alexis'

#prueba unitaria para la creación de super usuario
@pytest.mark.django_db
def test_superuser_creation():
    user = User.objects.create_superuser(
            username='alexis',
            email='alexis@duocuc.cl',
            password='12345'
    )
    assert user.is_superuser

#Verificar si un usuario existe
@pytest.mark.django_db
def test_user_exists():
    # Crear un usuario de prueba en la base de datos
    User.objects.create_user(username='jairo', password='123456')
    
    # Verificar si el usuario existe en la base de datos
    assert User.objects.filter(username='jairo').exists()
    
    # Verificar si un usuario que no existe en la base de datos no existe
    assert not User.objects.filter(username='nonexistentuser').exists()



