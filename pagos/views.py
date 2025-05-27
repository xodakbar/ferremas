from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from transbank.webpay.webpay_plus.transaction import Transaction, WebpayOptions
from transbank.common.integration_type import IntegrationType
import time
from carrito.utils import obtener_carrito, calcular_total
from .models import OrdenDeCompra 
from carrito.models import Carrito, ItemCarrito
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
    # Puedes agregar más códigos si los tienes documentados
}

# Configuración WebPay
commerce_code = settings.WEBPAY_CONFIG['COMMERCE_CODE']
api_key = settings.WEBPAY_CONFIG['API_KEY']
environment = IntegrationType.TEST if settings.WEBPAY_CONFIG['ENVIRONMENT'] == 'TEST' else IntegrationType.LIVE
tx = Transaction(WebpayOptions(commerce_code, api_key, environment))

def iniciar_pago(request):
    """Muestra el formulario inicial para iniciar el pago"""
    return render(request, 'pagos/iniciar_pago.html')

@csrf_exempt
def procesar_pago(request, carrito_id):
    """Versión unificada que usa carrito_id"""
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
            return_url=request.build_absolute_uri('/pagos/confirmacion/')
        )
        
        # Crea la orden
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

@csrf_exempt
def confirmar_pago(request):
    """Versión unificada de confirmación"""
    if request.method == 'GET':
        token = request.GET.get('token_ws')
        if not token:
            return render(request, 'pagos/fallo.html', {'error': 'Token no recibido'})
        
        try:
            # 1. Confirmar la transacción con WebPay
            response = tx.commit(token)
            
            # 2. Obtener la orden relacionada
            orden = OrdenDeCompra.objects.get(token=token)
            response_code = response.get('response_code')

            if response.get('response_code') == 0:
                # 3. Actualizar la orden con los datos de WebPay
                orden.estado = 'aprobado'
                fecha_str = response.get('transaction_date')
                if fecha_str:
                    try:
                        fecha_dt = datetime.strptime(fecha_str, '%Y-%m-%dT%H:%M:%S.%fZ')
                        orden.fecha_transaccion = make_aware(fecha_dt)
                    except (ValueError, TypeError) as e:
                        print(f"Error parseando fecha: {e}")
                        orden.fecha_transaccion = None
                orden.save()

                session_id = request.session.session_key
                if session_id:
                    from carrito.models import Carrito  # Asegúrate de importar correctamente

                    
                try:
                    
                    carrito = Carrito.objects.get(session_id=session_id)
                    carrito.items.all().delete()  # Borra todos los ItemCarrito asociados
                except Carrito.DoesNotExist:
                    pass

                
                # 4. Pasar todos los datos necesarios al template
                return render(request, 'pagos/exito.html', {
                    'orden': orden.buy_order,
                    'monto': orden.total,  # O response.get('amount') si prefieres
                    'fecha': orden.fecha_transaccion,
                    'fecha_str': response.get('transaction_date'),
                    'fecha_formateada': orden.fecha_formateada,
                    'respuesta_completa': response  # Opcional para debugging
                })
            else:
                mensaje_error = ERROR_CODES.get(response_code, f"Código de error desconocido: {response_code}")
                return render(request, 'pagos/fallo.html', {
                    'error': mensaje_error
                })
        except Exception as e:
            return render(request, 'pagos/fallo.html', {'error': str(e)})
                
        except Exception as e:
            return render(request, 'pagos/fallo.html', {'error': str(e)})
        

