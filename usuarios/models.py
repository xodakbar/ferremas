
# usuarios/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuario(AbstractUser):
    ROLES = (
        ('cliente', 'Cliente'),
        ('vendedor', 'Vendedor'),
        ('bodeguero', 'Bodeguero'),
        ('administrador', 'Administrador'),
        ('contador', 'Contador'),
    )
    rol = models.CharField(max_length=20, choices=ROLES)

    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.rol})"
