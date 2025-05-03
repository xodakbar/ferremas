from django.shortcuts import render,redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from rest_framework import viewsets
from .models import Usuario
from .serializers import UsuarioSerializer
from django.http import HttpResponse

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

    return render(request, 'registro.html')

def home(request):
    return render(request, 'usuarios/home.html')


