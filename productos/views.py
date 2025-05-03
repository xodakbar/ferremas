from django.shortcuts import render, get_object_or_404, redirect

# apps/productos/views.py

from rest_framework import viewsets
from .models import Producto
from .serializers import ProductoSerializer

class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer


def productos_template(request):
    return render(request, 'productos/listar.html')