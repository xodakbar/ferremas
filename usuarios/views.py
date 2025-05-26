from django.shortcuts import render,redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
from rest_framework import viewsets
from .models import Usuario
from .serializers import UsuarioSerializer
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer



def register_user(request):
    if request.method == 'POST':
        email = request.POST['email']
        nombre = request.POST['first_name']
        apellido = request.POST['last_name']
        password = request.POST['password']

        if Usuario.objects.filter(username=email).exists():
            return HttpResponse("Ya existe un usuario con este correo.")  # Mensaje simple, puedes redirigir o mejorar esto

        user = Usuario.objects.create_user(
            username=email,     # 👈 usamos email como username
            email=email,
            first_name=nombre,
            last_name=apellido,
            password=password,
            rol='cliente'       # 👈 asignación automática
        )
        return redirect('home')

    return render(request, 'usuarios/register.html')

def home(request):
    return render(request, 'usuarios/home.html')


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