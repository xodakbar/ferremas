from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from productos.views import (
    ProductoViewSet, lista_productos, agregar_producto,
    actualizar_stock, editar_producto, eliminar_producto,
    agregar_categoria, agregar_marca, ProductoCreateAPIView
)
from usuarios.views import (
    UsuarioViewSet, RegistroUsuarioView, home,
    login_view, acceso_denegado, logout_view
)
from carrito.views import agregar_al_carrito, ver_carrito, vaciar_carrito
from django.conf import settings
from django.conf.urls.static import static

router = DefaultRouter()
router.register(r'productos', ProductoViewSet)
router.register(r'usuarios', UsuarioViewSet)

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),

    # API con DRF
    path('api/', include(router.urls)),

    # Página de inicio
    path('', home, name='home'),

    # Usuarios
    path('api/', include('usuarios.urls')),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('acceso-denegado/', acceso_denegado, name='acceso-denegado'),

    # Productos (bodega)
    path('bodega/productos/', lista_productos, name='lista-productos-bodega'),
    path('bodega/productos/agregar/', agregar_producto, name='agregar-producto'),
    path('bodega/productos/editar/<int:producto_id>/', editar_producto, name='editar-producto'),
    path('productos/eliminar/<int:producto_id>/', eliminar_producto, name='eliminar-producto'),
    path('bodega/productos/actualizar-stock/<int:producto_id>/', actualizar_stock, name='actualizar-stock'),
    path('bodega/categorias/agregar/', agregar_categoria, name='agregar-categoria'),
    path('bodega/marcas/agregar/', agregar_marca, name='agregar-marca'),

    # API adicional
    path('api/productos/', ProductoCreateAPIView.as_view(), name='api-productos'),

    # Carrito
    path('agregar/', agregar_al_carrito, name='agregar_al_carrito'),
    path('carrito/', ver_carrito, name='ver_carrito'),
    path('carrito/vaciar/', vaciar_carrito, name='vaciar_carrito'),

    # Pagos con namespace
    path('pagos/', include(('pagos.urls', 'pagos'), namespace='pagos')),
]

# Media (para imágenes subidas)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
