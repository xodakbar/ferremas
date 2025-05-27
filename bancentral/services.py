# tipo_cambio/services.py
import requests
from datetime import datetime
from .models import TipoCambio

def actualizar_tipo_cambio():
    # URL de ejemplo (deberás adaptar a la API real)
    url = "https://api.bcentral.cl/servicio/tipo-cambio"  # pon la real

    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        # Aquí parseas el JSON según la estructura que entregue la API
        valor_usd = float(data['valor_dolar'])  # ejemplo
        tipo_cambio, created = TipoCambio.objects.get_or_create(moneda='USD')
        tipo_cambio.valor = valor_usd
        tipo_cambio.fecha_actualizacion = datetime.now()
        tipo_cambio.save()
        return tipo_cambio
    else:
        raise Exception("Error consultando API Banco Central")
