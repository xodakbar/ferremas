from rest_framework import viewsets
from rest_framework.response import Response
from .models import Carrito, ItemCarrito
from .serializers import CarritoSerializer, ItemCarritoSerializer
from productos.models import Producto
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render,redirect
from django.template.loader import render_to_string
from django.http import HttpResponse
from bancocentral.utils import obtener_valor_dolar_bcentral
from decimal import Decimal
from django.contrib.auth.decorators import login_required
import json
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required


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

@login_required
@csrf_protect
def agregar_al_carrito(request):
    if request.method == 'POST':
        try:
            datos = json.loads(request.body)
            producto_id = datos.get('producto_id')
            cantidad = int(datos.get('cantidad', 1))
        except (json.JSONDecodeError, TypeError, ValueError):
            return JsonResponse({'error': 'Datos inválidos'}, status=400)

        if not producto_id:
            return JsonResponse({'error': 'Debe seleccionar un producto'}, status=400)

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

        return JsonResponse({'success': f'Producto "{producto.nombre}" agregado al carrito'})

    return JsonResponse({'error': 'Método no permitido'}, status=405)

@login_required
def ver_carrito(request):
    if not request.session.session_key:
        request.session.create()
    
    session_id = request.session.session_key
    carrito, _ = Carrito.objects.get_or_create(session_id=session_id)
    items = ItemCarrito.objects.filter(carrito=carrito)
    
    total = sum(item.producto.precio * item.cantidad for item in items)
    valor_dolar = obtener_valor_dolar_bcentral()
    total_clp = total
    total_usd = None

    if valor_dolar and valor_dolar != 0:
        total_usd = Decimal(total) / Decimal(valor_dolar)

    context = {
        'items': items,
        'total': total,
        'carrito': carrito,  # Pasamos el objeto carrito completo
        'total_clp': total_clp,
        'total_usd': total_usd,

    }
    
    return render(request, 'carrito/carrito.html', context)

@login_required
def ver_carrito_ajax(request):
    # 1) Asegurar que haya session_key
    if not request.session.session_key:
        request.session.create()
    session_id = request.session.session_key

    # 2) Obtener carrito e ítems
    carrito, _ = Carrito.objects.get_or_create(session_id=session_id)
    items = ItemCarrito.objects.filter(carrito=carrito)

    # 3) Calcular total en CLP
    total = sum(item.producto.precio * item.cantidad for item in items)

    # 4) Intentar convertir a USD, si falla usar None
    try:
        valor_dolar = obtener_valor_dolar_bcentral()
        total_usd = (Decimal(total) / Decimal(valor_dolar)) if valor_dolar else None
    except Exception:
        total_usd = None

    # 5) Renderizar el partial con EXACTA ruta 'carrito/_contenido_carrito.html'
    html = render_to_string(
        'carrito/_contenido_carrito.html',
        {
            'items':      items,
            'total':      total,
            'total_usd':  total_usd,
            'carrito':    carrito,
        },
        request=request
    )

    return HttpResponse(html)

@login_required
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
