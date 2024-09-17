from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import CustomLoginView  # Importa la vista personalizada

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
]
