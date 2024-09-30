
from django.db import models

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True)

    def __str__(self):
        return self.nombre

from django.db import models
from django.contrib.auth.models import User
from .models import Producto  # Asegúrate de importar el modelo Producto

# Definimos el modelo Pedido, que relaciona productos con usuarios
class Pedido(models.Model):
    # Cada pedido está relacionado con un producto
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    
    # Cantidad del producto solicitado
    cantidad = models.IntegerField(default=1)
    
    # Fecha en que se realizó el pedido, se agrega automáticamente
    fecha = models.DateTimeField(auto_now_add=True)
    
    # Relación con el usuario que realiza el pedido
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    # Definimos cómo se va a mostrar el pedido en representaciones de string
    def __str__(self):
        return f"Pedido {self.id} - {self.producto.nombre} por {self.usuario.username}"

from django.db import models
from django.contrib.auth.models import User

class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField()
    juego_favorito = models.CharField(max_length=100)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)  # Ruta para el avatar

    def __str__(self):
        return self.user.username
