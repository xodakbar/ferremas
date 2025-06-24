# C:\Users\nachi\Documents\GitHub\ferremas\usuarios\tests.py

from django.test import TestCase, Client
from django.urls import reverse
from usuarios.models import Usuario
from django.contrib.messages import get_messages
from unittest.mock import patch

class LoginTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.username = 'testuser'
        self.password = 'testpass123'
        
        self.user = Usuario.objects.create(username=self.username)
        self.user.set_password(self.password)
        self.user.save()
        
        self.login_url = reverse('login')
        self.dashboard_url = reverse('home')

    def test_login_page_loads_correctly(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'usuarios/login.html')

    @patch('usuarios.views.requests')
    def test_successful_login(self, mock_requests):
        mock_requests.get.return_value.status_code = 200
        mock_requests.get.return_value.json.return_value = [{"nombre": "Producto Test"}]

        response = self.client.post(self.login_url, {'username': self.username, 'password': self.password}, follow=True)

        self.assertRedirects(response, self.dashboard_url, status_code=302, target_status_code=200)
        self.assertTrue(hasattr(response.wsgi_request, 'user') and response.wsgi_request.user.is_authenticated)
        self.assertEqual(response.wsgi_request.user, self.user)
        
        mock_requests.get.assert_called_once_with('http://127.0.0.1:8000/api/productos/')

    def test_failed_login_invalid_password(self):
        response = self.client.post(self.login_url, {'username': self.username, 'password': 'wrongpassword'}, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'usuarios/login.html')
        self.assertContains(response, "Credenciales inválidas") 

    def test_failed_login_non_existent_user(self):
        response = self.client.post(self.login_url, {'username': 'nonexistentuser', 'password': 'somepassword'}, follow=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'usuarios/login.html')
        self.assertContains(response, "Credenciales inválidas")

    @patch('usuarios.views.requests')
    def test_logout(self, mock_requests):
        mock_requests.get.return_value.status_code = 200
        mock_requests.get.return_value.json.return_value = [{"nombre": "Producto Test"}]

        login_response = self.client.post(self.login_url, {'username': self.username, 'password': self.password}, follow=True)
        self.assertTrue(login_response.wsgi_request.user.is_authenticated)

        logout_url = reverse('logout')
        
        response = self.client.post(logout_url, follow=True) 

        # CAMBIO CLAVE: Esperamos redirección a la raíz '/' en lugar de self.login_url
        self.assertRedirects(response, '/', status_code=302, target_status_code=200) 
        self.assertFalse(response.wsgi_request.user.is_authenticated)
        self.assertIsNone(self.client.session.get('_auth_user_id'))