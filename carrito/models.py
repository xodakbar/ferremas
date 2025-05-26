from django.db import models
from django.conf import settings

class Carrito(models.Model):
    session_id = models.CharField(max_length=100, null=True, blank=True)  # <- AGREGADO
    usuario = models.ForeignKey('usuarios.Usuario', null=True, blank=True, on_delete=models.SET_NULL)
    creado_en = models.DateTimeField(auto_now_add=True)
class ItemCarrito(models.Model):
    carrito = models.ForeignKey('Carrito', on_delete=models.CASCADE, related_name='items')
    producto = models.ForeignKey('productos.Producto', on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)

    def subtotal(self):
        return self.producto.precio * self.cantidad

