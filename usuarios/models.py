
# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuario(AbstractUser):
    ROLES = [
        ('cliente', 'Cliente'),
        ('vendedor', 'Vendedor'),
        ('admin', 'Administrador'),
        ('bodeguero', 'Bodeguero'),
        ('contador', 'Contador'),
    ]
    rol = models.CharField(max_length=20, choices=ROLES, default='cliente')

    def __str__(self):
        return f"{self.username} ({self.rol})"
