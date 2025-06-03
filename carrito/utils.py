from .models import Carrito

def obtener_carrito(request):
    if request.user.is_authenticated:
        carrito, _ = Carrito.objects.get_or_create(usuario=request.user)
    else:
        if not request.session.session_key:
            request.session.create()
        carrito, _ = Carrito.objects.get_or_create(
            session_id=request.session.session_key,
            usuario=None
        )
    return carrito

def calcular_total(carrito):
    return sum(item.subtotal() for item in carrito.items.all())