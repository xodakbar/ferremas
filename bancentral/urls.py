# tipo_cambio/urls.py
from django.urls import path
from .views import TipoCambioView

urlpatterns = [
    path('api/tipo-cambio/', TipoCambioView.as_view(), name='tipo-cambio'),
]
