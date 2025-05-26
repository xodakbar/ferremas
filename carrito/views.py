from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Carrito, ItemCarrito
from .serializers import CarritoSerializer, ItemCarritoSerializer
from productos.models import Producto
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
import json
from django.shortcuts import render


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
        try:
            data = json.loads(request.body)
            producto_id = data.get('producto_id')
            cantidad = int(data.get('cantidad', 1))

            if not producto_id:
                return JsonResponse({'error': 'producto_id es requerido'}, status=400)

            session_id = request.session.session_key or request.session.create()

            try:
                producto = Producto.objects.get(pk=producto_id)
            except Producto.DoesNotExist:
                return JsonResponse({'error': 'Producto no encontrado'}, status=404)

            carrito, _ = Carrito.objects.get_or_create(session_id=session_id)

            item, created = ItemCarrito.objects.get_or_create(
                carrito=carrito,
                producto=producto,
                defaults={'cantidad': cantidad}
            )

            if not created:
                item.cantidad += cantidad
                item.save()

            return JsonResponse({'mensaje': 'Producto agregado al carrito', 'carrito_id': carrito.id})

        except json.JSONDecodeError:
            return JsonResponse({'error': 'JSON inválido'}, status=400)

    return JsonResponse({'error': 'Método no permitido'}, status=405)

def ver_carrito(request):
    session_id = request.session.session_key or request.session.create()
    carrito = Carrito.objects.filter(session_id=session_id).first()
    items = ItemCarrito.objects.filter(carrito=carrito) if carrito else []

    total = 0
    for item in items:
        total += item.producto.precio * item.cantidad
    return render(request, 'carrito/carrito.html', {'items': items, 'total' : total})
