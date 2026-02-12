from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from transbank.webpay.webpay_plus.transaction import Transaction, WebpayOptions
from transbank.common.integration_type import IntegrationType
import time
from carrito.utils import calcular_total
from .models import OrdenDeCompra 
from carrito.models import Carrito
from datetime import datetime
from django.utils.timezone import make_aware

ERROR_CODES = {
    -1: "La transacción fue cancelada o no completada.",
    1: "Transacción rechazada sin motivo especificado.",
    2: "Transacción en proceso, por favor espere.",
    3: "Error en la transacción, intente nuevamente.",
    4: "Tarjeta vencida.",
    5: "Saldo insuficiente en la tarjeta.",
    6: "Tarjeta no autorizada para esta transacción.",
    7: "Rechazo por sospecha de fraude.",
    8: "Límite de transacciones diario excedido.",
    9: "Tarjeta no habilitada para compras online.",
    10: "Error de comunicación con la entidad financiera.",
}

commerce_code = settings.WEBPAY_CONFIG['COMMERCE_CODE']
api_key = settings.WEBPAY_CONFIG['API_KEY']
environment = IntegrationType.TEST if settings.WEBPAY_CONFIG['ENVIRONMENT'] == 'TEST' else IntegrationType.LIVE
tx = Transaction(WebpayOptions(commerce_code, api_key, environment))

def iniciar_pago(request):
    return render(request, 'pagos/iniciar_pago.html')

@csrf_exempt
def procesar_pago(request, carrito_id):
    carrito = get_object_or_404(Carrito, id=carrito_id)
    if not carrito.items.exists():
        return render(request, 'pagos/fallo.html', {'error': 'Carrito vacío'})

    total = calcular_total(carrito)
    buy_order = f"WP-{carrito.id}-{int(time.time()) % 1000}"[:26]

    try:
        response = tx.create(
            buy_order=buy_order,
            session_id=carrito.session_id or str(carrito.id),
            amount=int(total),
            return_url=request.build_absolute_uri(f'/pagos/confirmacion/{carrito.id}/')
        )

        orden = OrdenDeCompra.objects.create(
            carrito=carrito,
            total=total,
            buy_order=buy_order,
            token=response['token'],
            usuario=carrito.usuario
        )

        return render(request, 'pagos/formulario_pago.html', {
            'token': response['token'],
            'url_webpay': response['url'],
            'orden': orden,
            'items': carrito.items.all()
        })

    except Exception as e:
        return render(request, 'pagos/fallo.html', {'error': str(e)})

def confirmacion_pago(request, orden_id):
    orden = get_object_or_404(OrdenDeCompra, id=orden_id)
    return render(request, 'pagos/formulario_pago.html', {'orden': orden})

@csrf_exempt
def confirmar_pago(request):
    if request.method == 'GET':
        token = request.GET.get('token_ws')
        if not token:
            return render(request, 'pagos/fallo.html', {'error': 'Token no recibido'})
        
        try:
            response = tx.commit(token)
            orden = OrdenDeCompra.objects.get(token=token)
            response_code = response.get('response_code')

            if response_code == 0:
                orden.estado = 'aprobado'
                fecha_str = response.get('transaction_date')
                if fecha_str:
                    try:
                        fecha_dt = datetime.strptime(fecha_str, '%Y-%m-%dT%H:%M:%S.%fZ')
                        orden.fecha_transaccion = make_aware(fecha_dt)
                    except (ValueError, TypeError):
                        orden.fecha_transaccion = None
                orden.save()

                for item in orden.carrito.items.all():
                    producto = item.producto
                    if producto.stock >= item.cantidad:
                        producto.stock -= item.cantidad
                        producto.save()
                    else:
                        return render(request, 'pagos/fallo.html', {
                            'error': f"No hay stock suficiente para el producto {producto.nombre}."
                        })

                try:
                    carrito = Carrito.objects.get(session_id=request.session.session_key)
                    carrito.items.all().delete()
                except Carrito.DoesNotExist:
                    pass

                return render(request, 'pagos/exito.html', {
                    'orden': orden.buy_order,
                    'monto': orden.total,
                    'fecha': orden.fecha_transaccion,
                    'fecha_formateada': orden.fecha_formateada,
                    'respuesta_completa': response
                })
            else:
                mensaje_error = ERROR_CODES.get(response_code, f"Código de error desconocido: {response_code}")
                return render(request, 'pagos/fallo.html', {'error': mensaje_error})
        except Exception as e:
            return render(request, 'pagos/fallo.html', {'error': str(e)})

def exito_pago(request, token):
    orden = get_object_or_404(OrdenDeCompra, token=token, estado='aprobado')
    return render(request, 'pagos/exito.html', {'orden': orden})

def fallo_pago(request, token):
    orden = get_object_or_404(OrdenDeCompra, token=token, estado='rechazado')
    return render(request, 'pagos/fallo.html', {'orden': orden})
