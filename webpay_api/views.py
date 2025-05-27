from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from transbank.webpay.webpay_plus.transaction import Transaction
import uuid
from django.urls import reverse
import logging
from django.views.decorators.http import require_http_methods
from .webpay import webpay_options

logger = logging.getLogger(__name__)

# ✅ Instancia global del objeto transaction (puedes moverlo a otro archivo si prefieres)
transaction = Transaction.build_for_integration(
    commerce_code='597055555532',
    api_key='579B532A7440BB0C9079DED94D31EA1615BACEB56610332264630D42D0A36B1C'
)

@csrf_exempt
def create_payment(request):
    try:
        buy_order = f"BO{uuid.uuid4().hex[:12]}"
        session_id = request.session.session_key or str(uuid.uuid4())
        amount = 10000
        return_url = request.build_absolute_uri(reverse('webpay_response'))

        # ✅ Usamos la instancia transaction creada arriba
        response = transaction.create(buy_order, session_id, amount, return_url)

        request.session['last_buy_order'] = buy_order

        return render(request, 'webpay/redirect.html', {
            'webpay_url': response['url'],
            'token': response['token']
        })
    except Exception as e:
        logger.error(f"Error al crear pago: {str(e)}")
        return render(request, 'webpay/error.html', {
            'error': f"Error al iniciar el pago: {str(e)}"
        })


@csrf_exempt
@require_http_methods(["GET", "POST"])
def webpay_response(request):
    if request.method == "POST" and 'token_ws' in request.POST:
        try:
            token = request.POST['token_ws']
            tx = Transaction(options=webpay_options)
            response = tx.commit(token)

            stored_order = request.session.get('last_buy_order')
            if response['buy_order'] != stored_order:
                raise ValueError("Inconsistencia en buy_order")

            return render(request, 'webpay/resultado.html', {
                'buy_order': response['buy_order'],
                # otros datos que necesites
            })

        except Exception as e:
            return render(request, 'webpay/error.html', {
                'error': f"Error al procesar respuesta: {str(e)}"
            })

    else:
        # Simulación para pruebas sin token_ws (GET o POST sin token)
        fake_order = request.session.get('last_buy_order', 'ORDEN_SIMULADA_123')
        return render(request, 'webpay/resultado.html', {
            'buy_order': fake_order,
            'message': 'Simulación exitosa sin token_ws (modo prueba)'
        })
    
def payment_error(request):
    """Vista para mostrar errores generales de pago"""
    error_message = request.session.pop('payment_error', 'Ocurrió un error desconocido en el pago')
    return render(request, 'webpay/error.html', {
        'error': error_message,
        'back_url': reverse('create_payment')  # URL para reintentar
    })