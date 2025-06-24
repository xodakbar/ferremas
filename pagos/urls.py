from django.urls import path
from . import views

app_name = 'pagos'

urlpatterns = [
    path('iniciar/', views.iniciar_pago, name='iniciar_pago'),
    path('procesar/<int:carrito_id>/', views.procesar_pago, name='procesar_pago'),
    path('confirmacion/<int:orden_id>/', views.confirmacion_pago, name='confirmacion_pago'),
    path('confirmar/', views.confirmar_pago, name='confirmar_pago'),
    path('exito/<str:token>/', views.exito_pago, name='exito_pago'),
    path('fallo/<str:token>/', views.fallo_pago, name='fallo_pago'),
]