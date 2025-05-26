from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from productos.views import ProductoViewSet, lista_productos, agregar_producto,actualizar_stock,editar_producto
from usuarios.views import UsuarioViewSet, register_user, home, login_view, acceso_denegado

router = DefaultRouter()
router.register(r'productos', ProductoViewSet)  # Corregí el nombre de 'productos' (antes decía 'productos')
router.register(r'usuarios', UsuarioViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('', home, name='home'),  

    
    path('registro/', register_user, name='register_user'),
    path('login/', login_view, name='login'),
    path('acceso-denegado/', acceso_denegado, name='acceso-denegado'),
    
    # URLs para productos
    path('bodega/productos/', lista_productos, name='lista-productos-bodega'),
    path('bodega/productos/actualizar-stock/<int:producto_id>/', actualizar_stock, name='actualizar-stock'),
    path('bodega/productos/agregar/', agregar_producto, name='agregar-producto'),
    path('bodega/productos/editar/<int:producto_id>/', editar_producto, name='editar-producto'),
    
    # Puedes agregar también para editar si lo necesitas
    # path('productos/editar/<int:id>/', editar_producto, name='editar_producto'),
]