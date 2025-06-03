from rest_framework import serializers
from .models import Carrito, ItemCarrito

class ItemCarritoSerializer(serializers.ModelSerializer):
    subtotal = serializers.SerializerMethodField()

    class Meta:
        model = ItemCarrito
        fields = ['id', 'producto_id', 'nombre_producto', 'precio_unitario', 'cantidad', 'subtotal']

    def get_subtotal(self, obj):
        return obj.subtotal()

class CarritoSerializer(serializers.ModelSerializer):
    items = ItemCarritoSerializer(many=True, read_only=True)

    class Meta:
        model = Carrito
        fields = ['id', 'usuario', 'creado_en', 'items']
