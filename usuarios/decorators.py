from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import user_passes_test

def rol_requerido(*roles_requeridos):
    """
    Decorador para vistas basadas en funciones.
    Ejemplo de uso: @rol_requerido('administrador', 'contador')
    """
    def verificar_rol(user):
        if user.is_authenticated:
            return user.rol in roles_requeridos or user.is_superuser
        return False
    return user_passes_test(verificar_rol, login_url='login')

class RolRequiredMixin:
    """
    Mixin para vistas basadas en clases.
    Ejemplo de uso: class MiVista(RolRequiredMixin, View):
    """
    roles_requeridos = []
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        
        if (request.user.rol not in self.roles_requeridos 
            and not request.user.is_superuser):
            return self.handle_no_permission()
            
        return super().dispatch(request, *args, **kwargs)
    
    def handle_no_permission(self):
        from django.shortcuts import redirect
        return redirect('acceso-denegado')