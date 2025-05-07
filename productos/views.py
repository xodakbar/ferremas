from django.shortcuts import render, get_object_or_404, redirect

# apps/productos/views.py
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets
from .models import Producto
from .serializers import ProductoSerializer
from rest_framework.permissions import AllowAny

class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    permission_classes = [AllowAny]

def productos_template(request):
    return render(request, 'productos/listar.html')