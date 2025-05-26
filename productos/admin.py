from django.contrib import admin

from .models import Producto
from .models import Marca, Categoria

admin.site.register(Producto)
admin.site.register(Marca)
admin.site.register(Categoria)