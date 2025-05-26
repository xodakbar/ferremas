from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from transbank.webpay.webpay_plus.transaction import Transaction
from transbank.common.options import Options

class CustomOptions(Options):
    def header_api_key_name(self):
        return "Tbk-Api-Key-Id"

    def header_commerce_code_name(self):
        return "Tbk-Api-Key-Secret"

def pagar(request):
    buy_order = "orden123456"
    session_id = "sesion123456"
    amount = 10000
    return_url = request.build_absolute_uri('/webpay/commit/')

    options = Options(
        commerce_code="597055555532",
        api_key="fake_api_key_for_testing_purposes",
        integration_type=Options.integration_type
    )

    transaction = Transaction()

    create_response = transaction.create(
        buy_order=buy_order,
        session_id=session_id,
        amount=amount,
        return_url=return_url
    )

    # create_response tiene url y token
    return render(request, "webpay_redirect.html", {
        "url": create_response.url,
        "token": create_response.token,
    })

@csrf_exempt
def commit(request):
    token_ws = request.POST.get("token_ws")
    if not token_ws:
        return HttpResponse("No se recibió token_ws", status=400)

    transaction = Transaction()

    try:
        commit_response = transaction.commit(token_ws)
    except Exception as e:
        return HttpResponse(f"Error al confirmar transacción: {e}", status=500)

    if commit_response.status == "AUTHORIZED":
        return HttpResponse(f"Pago aprobado: Orden {commit_response.buy_order}, Monto {commit_response.amount}")
    else:
        return HttpResponse(f"Pago rechazado o estado: {commit_response.status}")
