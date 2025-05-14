from rest_framework import viewsets
from .models import Producto
from .serializers import ProductoSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly  # Mejor que AllowAny para producción
from django.shortcuts import render
from usuarios.decorators import rol_requerido
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.filter(activo=True)  # Solo productos activos
    serializer_class = ProductoSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]  # Seguridad básica
    
    # Filtros simples directamente en el viewset
    def get_queryset(self):
        queryset = super().get_queryset()
        categoria = self.request.query_params.get('categoria')
        if categoria:
            queryset = queryset.filter(categoria__iexact=categoria)
        return queryset

def productos_template(request):
    categoria = request.GET.get('categoria')
    productos = Producto.objects.filter(activo=True)
    
    if categoria:
        productos = productos.filter(categoria__iexact=categoria)
    
    return render(request, 'productos/listar.html', {
        'productos': productos,
        'categorias': Producto.objects.values_list('categoria', flat=True).distinct()
    })

@rol_requerido('bodeguero', 'administrador')
def lista_productos(request):
    productos = Producto.objects.filter(activo=True)
    
    # Filtros
    categoria = request.GET.get('categoria')
    if categoria:
        productos = productos.filter(categoria__iexact=categoria)
    
    # Búsqueda
    query = request.GET.get('q')
    if query:
        productos = productos.filter(nombre__icontains=query)
    
    return render(request, 'productos/lista_bodega.html', {
        'productos': productos,
        'categorias': Producto.objects.values_list('categoria', flat=True).distinct()
    })

@rol_requerido('bodeguero', 'administrador')
def agregar_producto(request):
    return render(request, 'productos/agregar_producto.html')

@rol_requerido('bodeguero', 'administrador')
def actualizar_stock(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    
    if request.method == 'POST':
        nuevo_stock = request.POST.get('stock')
        try:
            producto.stock = int(nuevo_stock)
            producto.save()
            messages.success(request, 'Stock actualizado correctamente')
        except ValueError:
            messages.error(request, 'El stock debe ser un número válido')
    
    return redirect('lista-productos-bodega')

