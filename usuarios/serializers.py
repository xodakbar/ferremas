# usuarios/serializers.py
from rest_framework import serializers
from .models import Usuario

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['first_name', 'last_name', 'email', 'password', 'rol']
        extra_kwargs = {
            'password': {'write_only': True},
            'rol': {'required': False},  # por si no se envía
        }

    def create(self, validated_data):
        password = validated_data.pop('password')
        email = validated_data.get('email')

        usuario = Usuario(
            username=email,
            email=email,
            first_name=validated_data.get('first_name'),
            last_name=validated_data.get('last_name'),
            rol=validated_data.get('rol', 'cliente')
        )
        usuario.set_password(password)
        usuario.save()
        return usuario

