from django.db import models

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)  # Hacer descripción opcional
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()  # Evita valores negativos
    categoria = models.CharField(max_length=50, db_index=True)  # Mejor para búsquedas
    activo = models.BooleanField(default=True)  # Para "borrado lógico"

    class Meta:
        ordering = ['nombre']  # Orden por defecto

    def __str__(self):
        return self.nombre