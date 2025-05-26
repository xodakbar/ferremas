# usuarios/serializers.py
from rest_framework import serializers
from .models import Usuario

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['first_name', 'last_name', 'email', 'password', 'rol']
        extra_kwargs = {
            'password': {'write_only': True},  # Asegura que la contraseña solo se pueda escribir
        }

    def create(self, validated_data):
        password = validated_data.pop('password')
        email = validated_data.get('email')
        usuario = Usuario(
        username=email,  # 👈 Esto es lo importante
        rol='cliente',
        **validated_data
    )
        usuario.set_password(password)  # Asegura que la contraseña se guarde de forma segura
        usuario.save()
        return usuario
