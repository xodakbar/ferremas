from rest_framework import serializers
from .models import Marca, Categoria, Producto, PrecioProducto

class MarcaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Marca
        fields = ['id', 'nombre']

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ['id', 'nombre']

class PrecioProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrecioProducto
        fields = ['fecha', 'valor']

class ProductoSerializer(serializers.ModelSerializer):
    marca = MarcaSerializer()
    categoria = CategoriaSerializer()
    precios = PrecioProductoSerializer(many=True, read_only=True)

    class Meta:
        model = Producto
        fields = [
            'id', 'nombre', 'descripcion', 'codigo_fabricante', 
            'marca', 'categoria', 'stock', 'activo', 'precios'
        ]
