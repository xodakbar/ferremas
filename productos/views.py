from rest_framework import viewsets
from .models import Producto
from .serializers import ProductoSerializer,PrecioProducto
from rest_framework.permissions import IsAuthenticatedOrReadOnly  # Mejor que AllowAny para producción
from django.shortcuts import render
from usuarios.decorators import rol_requerido
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from rest_framework import serializers
from django.db.models.signals import pre_save
from django.dispatch import receiver



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

class PrecioProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrecioProducto
        fields = ['fecha', 'valor']

class ProductoSerializer(serializers.ModelSerializer):
    precios = PrecioProductoSerializer(many=True, read_only=True)

    class Meta:
        model = Producto
        fields = [
            'id', 'nombre', 'descripcion', 'precio', 'stock',
            'categoria', 'codigo_fabricante', 'marca', 'activo', 'precios'
        ]

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

@rol_requerido('bodeguero', 'administrador')
def editar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    
    if request.method == 'POST':
        producto.nombre = request.POST.get('nombre', producto.nombre)
        producto.categoria = request.POST.get('categoria', producto.categoria)
        producto.precio = request.POST.get('precio', producto.precio)
        producto.stock = request.POST.get('stock', producto.stock)
        producto.descripcion = request.POST.get('descripcion', producto.descripcion)
        producto.marca = request.POST.get('marca', producto.marca)
        producto.codigo_fabricante = request.POST.get('codigo_fabricante', producto.codigo_fabricante)
        producto.save()
        
        messages.success(request, 'Producto actualizado correctamente')
        return redirect('lista-productos-bodega')
    
    return render(request, 'productos/editar_producto.html', {'producto': producto})

@receiver(pre_save, sender=Producto)
def guardar_precio_historial(sender, instance, **kwargs):
    if instance.pk:
        original = Producto.objects.get(pk=instance.pk)
        if instance.precio != original.precio:
            PrecioProducto.objects.create(producto=instance, valor=instance.precio)