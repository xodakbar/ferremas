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
from .models import Marca, Categoria


class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.filter(activo=True)
    serializer_class = ProductoSerializer  # Usa el serializer con nombres personalizados

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
        productos = productos.filter(categoria_id=categoria)
    
    categorias = Categoria.objects.all()
    
    return render(request, 'productos/lista_producto.html', {
        'productos': productos,
        'categorias': categorias
    })

@rol_requerido('bodeguero', 'administrador')
def lista_productos(request):
    productos = Producto.objects.filter(activo=True)
    
    categoria = request.GET.get('categoria')
    if categoria:
        productos = productos.filter(categoria_id=categoria)
    
    query = request.GET.get('q')
    if query:
        productos = productos.filter(nombre__icontains=query)
    
    categorias = Categoria.objects.all()
    
    return render(request, 'productos/listar_producto.html', {
        'productos': productos,
        'categorias': categorias
    })


@rol_requerido('bodeguero', 'administrador')
def agregar_producto(request):
    marcas = Marca.objects.all()
    categorias = Categoria.objects.all()
    return render(request, 'productos/agregar_producto.html', {'marcas': marcas, 'categorias': categorias})


@rol_requerido('bodeguero', 'administrador')
def editar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    marcas = Marca.objects.all()
    categorias = Categoria.objects.all()

    if request.method == "POST":
        producto.nombre = request.POST.get("nombre")
        producto.descripcion = request.POST.get("descripcion")
        producto.precio = float(request.POST.get("precio") or 0)
        producto.stock = int(request.POST.get("stock") or 0)
        producto.codigo_fabricante = request.POST.get("codigo_fabricante")
        producto.marca_id = int(request.POST.get("marca"))
        producto.categoria_id = int(request.POST.get("categoria"))
        producto.activo = "activo" in request.POST

        producto.save()
        return redirect('lista-productos-bodega')

    return render(request, "productos/editar_producto.html", {
        "producto": producto,
        "marcas": marcas,
        "categorias": categorias,
    })



@rol_requerido('bodeguero', 'administrador')
def eliminar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)

    if request.method == "POST":
        producto.delete()
        messages.success(request, "Producto eliminado correctamente.")
        return redirect('lista-productos-bodega')

    return render(request, "productos/confirmar_eliminar.html", {"producto": producto})

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

@receiver(pre_save, sender=Producto)
def guardar_precio_historial(sender, instance, **kwargs):
    if instance.pk:
        original = Producto.objects.get(pk=instance.pk)
        if instance.precio != original.precio:
            PrecioProducto.objects.create(producto=instance, valor=instance.precio)