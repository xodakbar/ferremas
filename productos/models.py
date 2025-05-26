from django.db import models

class Marca(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre

class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    marca = models.ForeignKey(Marca, on_delete=models.CASCADE, related_name='productos')
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, related_name='productos')
    codigo_fabricante = models.CharField(max_length=50, unique=True)
    stock = models.PositiveIntegerField()
    activo = models.BooleanField(default=True)

    class Meta:
        ordering = ['nombre']

    def __str__(self):
        return f"{self.nombre} ({self.marca})"

class PrecioProducto(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='precios')
    fecha = models.DateTimeField(auto_now_add=True)
    valor = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        ordering = ['-fecha']

    def __str__(self):
        return f"{self.producto.nombre} - {self.valor} ({self.fecha.date()})"
