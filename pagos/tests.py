from django.test import TestCase, Client
from django.urls import reverse
from .models import OrdenDeCompra
from carrito.models import Carrito
from django.contrib.auth import get_user_model

User = get_user_model()

class PagosTests(TestCase):
    def setUp(self):
        # Crear usuario con el modelo correcto
        self.usuario = User.objects.create_user(username='testuser', password='12345')

        # Crear carrito
        self.carrito = Carrito.objects.create(usuario=self.usuario, session_id='testsession123')

        # Crear orden simulada
        self.orden = OrdenDeCompra.objects.create(
            carrito=self.carrito,
            total=2000,
            buy_order='WP-1-123',
            token='token123',
            usuario=self.usuario,
            estado='aprobado'
        )
        
        self.client = Client()
    
    def test_confirmacion_pago_view(self):
        url = reverse('pagos:confirmacion_pago', args=[self.orden.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('orden', response.context)
    
    def test_exito_pago_view(self):
        url = reverse('pagos:exito_pago', args=[self.orden.token])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('orden', response.context)
        self.assertEqual(response.context['orden'], self.orden)
    
    def test_fallo_pago_view(self):
        orden_fallo = OrdenDeCompra.objects.create(
            carrito=self.carrito,
            total=2000,
            buy_order='WP-2-123',
            token='tokenrechazado',
            usuario=self.usuario,
            estado='rechazado'
        )
        url = reverse('pagos:fallo_pago', args=[orden_fallo.token])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('orden', response.context)
        self.assertEqual(response.context['orden'], orden_fallo)
