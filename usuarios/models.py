
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
    rol = models.CharField(max_length=20, choices=ROLES, default='cliente')  # 👈 esto asigna cliente por defecto


    USERNAME_FIELD = 'username'  # Mantienes el login con username (en este caso, será el email)
    REQUIRED_FIELDS = ['email']
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.rol})"
