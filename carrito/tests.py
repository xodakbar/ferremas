from django.test import TestCase, Client
from django.urls import reverse
from usuarios.models import Usuario
from productos.models import Producto, Categoria, Marca
from carrito.models import Carrito, ItemCarrito
from django.core.files.uploadedfile import SimpleUploadedFile
from decimal import Decimal


class CarritoTemplateTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Crear usuario
        cls.user = Usuario.objects.create_user(
            username='testuser',
            password='testpassword123',
            email='test@example.com'
        )
        
        # Crear categoría y marca
        cls.categoria = Categoria.objects.create(nombre='Herramientas')
        cls.marca = Marca.objects.create(nombre='Bosch')
        
        # Crear productos de prueba con códigos únicos
        cls.producto1 = Producto.objects.create(
            nombre='Martillo',
            precio=Decimal('10.50'),
            stock=100,
            categoria=cls.categoria,
            marca=cls.marca,
            codigo_producto='MART-001',
            codigo_fabricante='FAB-001',
            imagen=SimpleUploadedFile("martillo.jpg", b"file_content", content_type="image/jpeg")
        )
        cls.producto2 = Producto.objects.create(
            nombre='Destornillador',
            precio=Decimal('5.75'),
            stock=50,
            categoria=cls.categoria,
            marca=cls.marca,
            codigo_producto='DEST-001',
            codigo_fabricante='FAB-002'
        )

    def setUp(self):
        self.client = Client()
        self.client.login(username='testuser', password='testpassword123')
        session = self.client.session
        session.save()

    def test_carrito_vacio(self):
        """Test que verifica el template cuando el carrito está vacío"""
        response = self.client.get(reverse('ver_carrito'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'carrito/carrito.html')
        self.assertContains(response, "Tu carrito está vacío")
        self.assertContains(response, "Descubrir productos")

    def test_carrito_con_items(self):
        """Test que verifica el template cuando hay items en el carrito"""
        session_id = self.client.session.session_key
        carrito = Carrito.objects.create(session_id=session_id)
        ItemCarrito.objects.create(
            carrito=carrito,
            producto=self.producto1,
            cantidad=2,
            precio=self.producto1.precio
        )
        ItemCarrito.objects.create(
            carrito=carrito,
            producto=self.producto2,
            cantidad=1,
            precio=self.producto2.precio
        )

        response = self.client.get(reverse('ver_carrito'))
        self.assertEqual(response.status_code, 200)

        # Verificar productos y cantidades
        self.assertContains(response, self.producto1.nombre)
        self.assertContains(response, self.producto2.nombre)
        self.assertContains(response, "2")
        self.assertContains(response, "1")

        # Verificar precios unitarios
        self.assertContains(response, "$10,50")
        self.assertContains(response, "$5,75")

        # Verificar subtotales
        self.assertContains(response, "$21,00")
        self.assertContains(response, "$5,75")

        # Verificar total
        self.assertContains(response, "$27")

        # Verificar botones
        self.assertContains(response, "Seguir comprando")
        self.assertContains(response, "Pagar $27 con WebPay")
        self.assertContains(response, "Vaciar carrito")

    def test_imagen_producto_en_carrito(self):
        """Test que verifica que se muestra la imagen del producto"""
        session_id = self.client.session.session_key
        carrito = Carrito.objects.create(session_id=session_id)
        ItemCarrito.objects.create(
            carrito=carrito,
            producto=self.producto1,
            cantidad=1,
            precio=self.producto1.precio
        )

        response = self.client.get(reverse('ver_carrito'))
        self.assertContains(response, self.producto1.imagen.url)

    def test_formato_numeros_grandes(self):
        """Test que verifica el formato de números grandes con espacio no rompible"""
        producto3 = Producto.objects.create(
            nombre='Taladro Profesional',
            precio=Decimal('125000.99'),
            stock=10,
            categoria=self.categoria,
            marca=self.marca,
            codigo_producto='TAL-001',
            codigo_fabricante='FAB-003'
        )

        session_id = self.client.session.session_key
        carrito = Carrito.objects.create(session_id=session_id)
        ItemCarrito.objects.create(
            carrito=carrito,
            producto=producto3,
            cantidad=3,
            precio=producto3.precio
        )

        response = self.client.get(reverse('ver_carrito'))
        response_content = response.content.decode('utf-8')

        nbsp = "\u00a0"
        self.assertIn(f"$125{nbsp}000,99", response_content)  # Precio unitario
        self.assertIn(f"$375{nbsp}002,97", response_content)  # Subtotal
        self.assertIn(f"$375{nbsp}003", response_content)     # Total redondeado
        self.assertIn(f"Pagar $375{nbsp}003 con WebPay", response_content)

    def test_boton_pago_webpay(self):
        """Test que verifica el botón de pago con WebPay"""
        session_id = self.client.session.session_key
        carrito = Carrito.objects.create(session_id=session_id)
        ItemCarrito.objects.create(
            carrito=carrito,
            producto=self.producto1,
            cantidad=1,
            precio=self.producto1.precio
        )

        response = self.client.get(reverse('ver_carrito'))
        self.assertContains(response, "Pagar $11 con WebPay")
        self.assertContains(response, reverse('procesar_pago', args=[carrito.id]))

    def test_vaciar_carrito(self):
        """Test que verifica el botón de vaciar carrito"""
        session_id = self.client.session.session_key
        carrito = Carrito.objects.create(session_id=session_id)
        ItemCarrito.objects.create(
            carrito=carrito,
            producto=self.producto1,
            cantidad=1,
            precio=self.producto1.precio
        )

        response = self.client.get(reverse('ver_carrito'))
        self.assertContains(response, "Vaciar carrito")
        self.assertContains(response, reverse('vaciar_carrito'))

    def test_conversion_moneda(self):
        """Test que verifica la conversión a USD"""
        session_id = self.client.session.session_key
        carrito = Carrito.objects.create(session_id=session_id)
        ItemCarrito.objects.create(
            carrito=carrito,
            producto=self.producto1,
            cantidad=1,
            precio=self.producto1.precio
        )

        response = self.client.get(reverse('ver_carrito'))
        self.assertContains(response, "Total a pagar en USD")
        self.assertContains(response, "$ USD")
