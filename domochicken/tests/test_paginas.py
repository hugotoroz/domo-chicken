import pytest

from core.models import User
from django.test import Client, TestCase

class test_carga_index(TestCase):
    def setUp(self):
        self.client = Client()

    def test_template_content(self):
        response = self.client.get('')
        assert response.status_code == 200

class test_carga_catalogo(TestCase):
    def setUp(self):
        self.client = Client()

    def test_template_content(self):
        response = self.client.get('/catalogo/')
        assert response.status_code == 200

class test_carga_login(TestCase):
    def setUp(self):
        self.client = Client()

    def test_template_content(self):
        response = self.client.get('/iniciar_sesion/')
        assert response.status_code == 200

class test_carga_registro(TestCase):
    def setUp(self):
        self.client = Client()

    def test_template_content(self):
        response = self.client.get('/registrarse/')
        assert response.status_code == 200

class test_buscar_url_fallido(TestCase):
    def setUp(self):
        self.client = Client()

    def test_template_content(self):
        response = self.client.get('/urlquenoexiste/')
        assert response.status_code == 404