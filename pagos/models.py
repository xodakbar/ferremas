from django.db import models
from carrito.models import Carrito

class OrdenDeCompra(models.Model):
    ESTADOS = (
        ('pendiente', 'Pendiente'),
        ('aprobado', 'Aprobado'),
        ('rechazado', 'Rechazado'),
    )
    
    carrito = models.ForeignKey(Carrito, on_delete=models.PROTECT)
    usuario = models.ForeignKey('usuarios.Usuario', null=True, on_delete=models.SET_NULL)
    session_id = models.CharField(max_length=100, null=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    buy_order = models.CharField(max_length=26, unique=True)
    token = models.CharField(max_length=200, null=True)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')
    creado_en = models.DateTimeField(auto_now_add=True)
    fecha_transaccion = models.DateTimeField(null=True, blank=True)
    @property
    def fecha_formateada(self):
        if self.fecha_transaccion:
            try:
                return self.fecha_transaccion.strftime("%d/%m/%Y %H:%M")
            except AttributeError:
                return str(self.fecha_transaccion)
        return "No disponible"
    
    class Meta:
        verbose_name = 'Orden de Compra'
        verbose_name_plural = 'Órdenes de Compra'
    
    def __str__(self):
        return f"Orden {self.buy_order} - {self.estado}"