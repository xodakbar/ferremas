from django.urls import path
from . import views

# pagos/urls.py
urlpatterns = [
    path('', views.confirmar_pago, name='iniciar_pago'),
    path('procesar/<int:carrito_id>/', views.procesar_pago, name='procesar_pago'),
    path('confirmacion/', views.confirmar_pago, name='confirmar_pago'),
]