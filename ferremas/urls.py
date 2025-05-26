from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from carrito import views
from productos.views import ProductoViewSet, lista_productos, agregar_producto,actualizar_stock,editar_producto, eliminar_producto
from usuarios.views import UsuarioViewSet, register_user,home, login_view, acceso_denegado
from carrito.views import agregar_al_carrito, ver_carrito
from carrito.webpay import pagar, commit

router = DefaultRouter()
router.register(r'productos', ProductoViewSet)  # Corregí el nombre de 'productos' (antes decía 'productos')
router.register(r'usuarios', UsuarioViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('', home, name='home'),  

    # URLs para usuarios
    
    path('registro/', register_user, name='register_user'),
    path('login/', login_view, name='login'),
    path('acceso-denegado/', acceso_denegado, name='acceso-denegado'),
    
    # URLs para productos
    path('bodega/productos/', lista_productos, name='lista-productos-bodega'),
    path('bodega/productos/actualizar-stock/<int:producto_id>/', actualizar_stock, name='actualizar-stock'),
    path('bodega/productos/agregar/', agregar_producto, name='agregar-producto'),
    path('bodega/productos/editar/<int:producto_id>/', editar_producto, name='editar-producto'),
    path('productos/eliminar/<int:producto_id>/', eliminar_producto, name='eliminar-producto'),

    #URLs para carrito
    path('agregar/', agregar_al_carrito, name='agregar_al_carrito'),
    path('carrito/', ver_carrito, name='ver_carrito'),

    #URLs WebPay
    path('webpay/pagar/', pagar, name='iniciar_pago'),
    path('webpay/commit/', commit, name='commit_pago'),
]