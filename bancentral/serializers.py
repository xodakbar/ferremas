# tipo_cambio/serializers.py
from rest_framework import serializers
from .models import TipoCambio

class TipoCambioSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoCambio
        fields = ['moneda', 'valor', 'fecha_actualizacion']
