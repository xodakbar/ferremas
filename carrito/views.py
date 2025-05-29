from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Carrito, ItemCarrito
from .serializers import CarritoSerializer, ItemCarritoSerializer
from productos.models import Producto
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render,redirect
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404

class CarritoViewSet(viewsets.ModelViewSet):
    queryset = Carrito.objects.all()
    serializer_class = CarritoSerializer

    def get_queryset(self):
        return self.queryset.filter(usuario=self.request.user)


class ItemCarritoViewSet(viewsets.ModelViewSet):
    queryset = ItemCarrito.objects.all()
    serializer_class = ItemCarritoSerializer

    def create(self, request, *args, **kwargs):
        try:
            producto_id = request.data.get("producto_id")
            cantidad = int(request.data.get("cantidad", 1))

            if not producto_id:
                return Response({"error": "producto_id es requerido"}, status=400)

            try:
                producto_db = Producto.objects.get(pk=producto_id)
            except Producto.DoesNotExist:
                return Response({"error": "Producto no encontrado"}, status=404)

            # Carrito por usuario autenticado o sesión
            if request.user.is_authenticated:
                carrito, _ = Carrito.objects.get_or_create(usuario=request.user)
            else:
                session_id = request.session.session_key or request.session.create()
                carrito, _ = Carrito.objects.get_or_create(session_id=session_id)

            # Buscar o crear item
            item, created = ItemCarrito.objects.get_or_create(
                carrito=carrito,
                producto=producto_db,
                defaults={"cantidad": cantidad}
            )

            if not created:
                item.cantidad += cantidad
                item.save()

            return Response(ItemCarritoSerializer(item).data, status=201)

        except Exception as e:
            return Response({"error": str(e)}, status=500)


@csrf_protect
def agregar_al_carrito(request):
    if request.method == 'POST':
        producto_id = request.POST.get('producto_id')
        cantidad = int(request.POST.get('cantidad', 1))

        if not producto_id:
            messages.error(request, 'Debe seleccionar un producto.')
            return redirect('lista-productos-bodega')  # O la página que corresponda

        producto = get_object_or_404(Producto, pk=producto_id)

        session_id = request.session.session_key
        if not session_id:
            request.session.create()
            session_id = request.session.session_key

        carrito, _ = Carrito.objects.get_or_create(session_id=session_id)

        item, created = ItemCarrito.objects.get_or_create(
            carrito=carrito,
            producto=producto,
            defaults={'cantidad': cantidad, 'precio': producto.precio}
        )

        if not created:
            item.cantidad += cantidad
            item.save()

        messages.success(request, f'Producto "{producto.nombre}" agregado al carrito.')

        # Redirigir a la página del carrito o la página anterior
        return redirect('ver_carrito')

    # Si no es POST, redirige a productos
    return redirect('lista-productos-bodega')

def ver_carrito(request):
    if not request.session.session_key:
        request.session.create()
    
    session_id = request.session.session_key
    carrito, _ = Carrito.objects.get_or_create(session_id=session_id)
    items = ItemCarrito.objects.filter(carrito=carrito)
    
    total = sum(item.producto.precio * item.cantidad for item in items)
    # Obtener tipo de cambio USD
    total_clp = total
    tipo_cambio_usd = obtener_tipo_cambio_usd()

    if tipo_cambio_usd:
        total_usd = total_clp / tipo_cambio_usd
    else:
        total_usd = None  # o mostrar mensaje "No disponible"
    context = {
        'items': items,
        'total': total,
        'carrito': carrito,  # Pasamos el objeto carrito completo
        'total_clp': total_clp,
        'total_usd': total_usd,
        'tipo_cambio_usd': tipo_cambio_usd,
    }
    return render(request, 'carrito/carrito.html', context)

def vaciar_carrito(request):
    session_id = request.session.session_key
    if session_id:
        try:
            carrito = Carrito.objects.get(session_id=session_id)
            # Borra todos los items del carrito
            carrito.items.all().delete()
            # Opcional: eliminar el carrito mismo
            # carrito.delete()
        except Carrito.DoesNotExist:
            pass
    return redirect('ver_carrito')  # Redirige a la página del carrito
