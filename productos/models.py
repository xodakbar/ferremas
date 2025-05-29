from django.db import models
from decimal import Decimal
from bancocentral.utils import obtener_valor_dolar_bcentral

class Marca(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre

class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    codigo_producto = models.CharField(max_length=50, unique=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    marca = models.ForeignKey(Marca, on_delete=models.CASCADE, related_name='productos')
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, related_name='productos')
    codigo_fabricante = models.CharField(max_length=50, unique=True)
    stock = models.PositiveIntegerField()
    activo = models.BooleanField(default=True)
    imagen = models.ImageField(upload_to='productos/', null=True, blank=True)

    class Meta:
        ordering = ['nombre']


    def __str__(self):
        return f"{self.nombre} ({self.marca})"
    
    def precio_en_dolares(self):
        valor_dolar = obtener_valor_dolar_bcentral()
        if valor_dolar:
            return Decimal(self.precio) / Decimal(valor_dolar)
        return None

class PrecioProducto(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='precios')
    fecha = models.DateTimeField(auto_now_add=True)
    valor = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        ordering = ['-fecha']

    def __str__(self):
        return f"{self.producto.nombre} - {self.valor} ({self.fecha.date()})"
