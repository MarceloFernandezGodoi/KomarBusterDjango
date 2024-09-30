from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
from .views import CustomLoginView  # Importa la vista personalizada
from rest_framework.routers import DefaultRouter
from .views import ProductoViewSet, PedidoViewSet
from .views import get_free_games


from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

# Creamos un router que se encargará de las rutas de los ViewSets
router = DefaultRouter()
router.register(r'productos', ProductoViewSet)  # Registrar el ViewSet de Producto
router.register(r'pedidos', PedidoViewSet)  # Registrar el ViewSet de Pedido


urlpatterns = [
    path('', views.home, name='home'),  
    path('perfil/', views.perfil_usuario, name='perfil_usuario'),
    path('registro/', views.registro, name='registro'),
    path('protegida/', views.vista_protegida, name='protegida'),
    path('productos/', views.listar_productos, name='listar_productos'),
    path('productos/crear/', views.crear_producto, name='crear_producto'),
    path('productos/editar/<int:pk>/', views.editar_producto, name='editar_producto'),
    path('productos/eliminar/<int:pk>/', views.eliminar_producto, name='eliminar_producto'),
    path('login/', CustomLoginView.as_view(), name='login'), # Aquí usamos la vista personalizada
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='Juegos/password_reset.html'), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='Juegos/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='Juegos/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='Juegos/password_reset_complete.html'), name='password_reset_complete'),
    path('prueba-correo/', views.enviar_correo_prueba, name='prueba_correo'),
    path('carrito/', views.ver_carrito, name='ver_carrito'),
    path('carrito/agregar/<int:producto_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('carrito/eliminar/<int:producto_id>/', views.eliminar_del_carrito, name='eliminar_del_carrito'),
    path('carrito/vaciar/', views.vaciar_carrito, name='vaciar_carrito'),
    path('carrito/actualizar/<int:producto_id>/', views.actualizar_cantidad_carrito, name='actualizar_cantidad_carrito'),
    path('api/productos/', views.productos_api, name='productos_api'),
    path('api/productos/<int:pk>/', views.productos_api, name='producto_detalle'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/', include(router.urls)),  # Incluir las rutas del router en la URL base 'api/'
    path('pedidos/', views.ListaPedidosView.as_view(), name='lista_pedidos'),
    path('pedidos/crear/', views.CrearPedidoView.as_view(), name='crear_pedido'),
    path('pedidos/editar/<int:pk>/', views.EditarPedidoView.as_view(), name='editar_pedido'),
    path('pedidos/eliminar/<int:pk>/', views.EliminarPedidoView.as_view(), name='eliminar_pedido'),
    path('noticias/', views.noticias, name='noticias'),
    path('free-games/', views.get_free_games, name='free_games'),

] 