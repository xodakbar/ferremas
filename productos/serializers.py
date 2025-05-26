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
    Fecha = serializers.DateTimeField(source='fecha')
    Valor = serializers.DecimalField(source='valor', max_digits=10, decimal_places=2)
    class Meta:
        model = PrecioProducto
        fields = ['Fecha', 'Valor']

class ProductoSerializer(serializers.ModelSerializer):
    # Para lectura (solo lectura)
    marca = MarcaSerializer(read_only=True)
    categoria = CategoriaSerializer(read_only=True)
    precios = PrecioProductoSerializer(many=True, read_only=True)

    # Para escritura: aceptamos IDs para marca y categoria
    marca_id = serializers.PrimaryKeyRelatedField(
        queryset=Marca.objects.all(), source='marca', write_only=True
    )
    categoria_id = serializers.PrimaryKeyRelatedField(
        queryset=Categoria.objects.all(), source='categoria', write_only=True
    )

    class Meta:
        model = Producto
        fields = [
            'id', 'codigo_producto','nombre',  'descripcion', 'codigo_fabricante', 'precio', 
            'marca', 'categoria', 'marca_id', 'categoria_id',
            'stock', 'activo', 'precios'
        ]


