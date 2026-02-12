# productos/forms.py
from django import forms
from .models import Producto, Categoria, Marca

class ProductoForm(forms.ModelForm):
    # Si quieres personalizar campos o añadir validaciones específicas, hazlo aquí.
    # Por ejemplo, para asegurar que stock y precio sean positivos:
    stock = forms.IntegerField(min_value=0)
    precio = forms.DecimalField(min_value=0.0, decimal_places=2)

    class Meta:
        model = Producto
        fields = ['nombre', 'descripcion', 'precio', 'stock', 'categoria', 'marca', 'imagen', 'activo']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['categoria'].queryset = Categoria.objects.all()
        self.fields['marca'].queryset = Marca.objects.all()