from django.shortcuts import render,redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
from rest_framework import viewsets
from .models import Usuario
from .serializers import UsuarioSerializer
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
import requests
from django.contrib.auth import logout
from django.views.decorators.http import require_POST
from django.conf import settings


class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer



def register_user(request):

    return render(request, 'usuarios/register.html')

def home(request):
    resp = requests.get('http://127.0.0.1:8000/api/productos/')
    productos = resp.json() if resp.status_code == 200 else []

    return render(request, 'usuarios/home.html', {'productos': productos ,'MEDIA_URL': settings.MEDIA_URL})


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']  # es tu email en este caso
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'usuarios/login.html', {'error': 'Credenciales inválidas'})
    return render(request, 'usuarios/login.html')


def acceso_denegado(request):
    return render(request, 'usuarios/acceso_denegado.html', status=403)

@require_POST
def logout_view(request):
    logout(request)
    return redirect('home')