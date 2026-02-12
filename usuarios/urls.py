from django.urls import path
from .views import RegistroUsuarioView, registro_html

urlpatterns = [
    path('register/', RegistroUsuarioView.as_view(), name='register'),
    path('registro/', registro_html, name='registro_html'),
]
