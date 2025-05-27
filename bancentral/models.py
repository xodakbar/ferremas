# tipo_cambio/models.py
from django.db import models

class TipoCambio(models.Model):
    moneda = models.CharField(max_length=10, unique=True)  # Ej: "USD"
    valor = models.DecimalField(max_digits=10, decimal_places=4)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.moneda}: {self.valor} (actualizado {self.fecha_actualizacion})"
