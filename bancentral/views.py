# tipo_cambio/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import TipoCambio
from .serializers import TipoCambioSerializer
import requests


class TipoCambioView(APIView):
    def get(self, request):
        try:
            tipo_cambio = TipoCambio.objects.get(moneda='USD')
        except TipoCambio.DoesNotExist:
            return Response({"error": "Tipo de cambio no disponible"}, status=404)
        serializer = TipoCambioSerializer(tipo_cambio)
        return Response(serializer.data)


def obtener_tipo_cambio_usd():
    url = "/api/tipo-cambio/"
    try:
        resp = requests.get(url)
        if resp.status_code == 200:
            data = resp.json()
            return float(data['valor'])
        else:
            # En caso de error, usar valor por defecto o lanzar excepción
            return None
    except requests.RequestException:
        return None