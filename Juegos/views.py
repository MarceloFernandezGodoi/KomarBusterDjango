from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from .models import Producto
from .forms import ProductoForm
from django.http import HttpResponse
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect

@login_required
def home(request):
    context = {
        'is_superuser': request.user.is_superuser,
    }
    return render(request, 'Juegos/home.html', context)

def registro(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user=form.save()
            login(request, user)
            return redirect('home')
        else: 
            form =UserCreationForm()
            return render(request, 'Juegos/registro.html', {'form': form})
        
@login_required
def vista_protegida(request):
    return render(request, 'Juegos/protegida.html')

@login_required
def listar_productos(request):
    productos = Producto.objects.all()
    return render(request, 'Juegos/listar.html', {'productos': productos})

@login_required
def crear_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_productos')
    else:
        form = ProductoForm()
    return render(request, 'Juegos/crear.html', {'form': form})

@login_required
def editar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('listar_productos')
    else:
        form = ProductoForm(instance=producto)
    return render(request, 'Juegos/editar.html', {'form': form})

@login_required
def eliminar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        producto.delete()
        return redirect('listar_productos')
    return render(request, 'Juegos/eliminar.html', {'producto': producto})



def registro(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Iniciar sesión automáticamente después de registrar
            return redirect('listar_productos')
    else:
        form = UserCreationForm()
    return render(request, 'Juegos/registro.html', {'form': form})


class CustomLoginView(LoginView):
    template_name = 'Juegos/login.html'

    def get_success_url(self):
        # Si es superusuario, redirigir al panel de administración
        if self.request.user.is_superuser:
            return '/Juegos/'  # Puedes redirigir a cualquier otra página especial para superusuarios
        # Si es un usuario normal, redirigir a la lista de productos
        return reverse('home')
    

from django.contrib.auth.models import User

@login_required
def perfil_usuario(request):
    if request.user.is_superuser:
        usuarios = User.objects.all()
    else:
        usuarios = None

    context = {
        'user': request.user,
        'usuarios': usuarios,
    }
    return render(request, 'Juegos/perfil.html', context)


from django.core.mail import send_mail
from django.http import HttpResponse

def enviar_correo_prueba(request):
    send_mail(
        'Prueba de correo',  # Asunto
        'Este es un correo de prueba.',  # Cuerpo del mensaje
        'djangoproyecto348@gmail.com',  # Correo remitente
        ['fr.tossi@profesor.duoc.cl'],  # Correo del destinatario
        fail_silently=False,
    )
    return HttpResponse('Correo enviado con éxito')


from django.shortcuts import get_object_or_404, redirect, render

def agregar_al_carrito(request, producto_id):
    # Obtener el producto o devolver un error 404 si no existe
    producto = get_object_or_404(Producto, id=producto_id)
    
    # Convertir el producto_id a cadena, ya que las claves en la sesión son strings
    producto_id_str = str(producto_id)
    
    # Obtener el carrito de la sesión, si no existe, inicializarlo como un diccionario vacío
    carrito = request.session.get('carrito', {})
    
    # Si el producto ya está en el carrito, incrementar la cantidad
    if producto_id_str in carrito:
        carrito[producto_id_str]['cantidad'] += 1
    else:
        # Agregar el producto al carrito con la cantidad inicial de 1
        carrito[producto_id_str] = {
            'nombre': producto.nombre,
            'precio': float(producto.precio),
            'cantidad': 1,
        }
    
    # Guardar el carrito en la sesión
    request.session['carrito'] = carrito
    
    return redirect('listar_productos')

def ver_carrito(request):
    # Obtener el carrito de la sesión, si no existe, inicializarlo como un diccionario vacío
    carrito = request.session.get('carrito', {})
    
    total = sum(item['precio'] * item['cantidad'] for item in carrito.values())  # Calcular el total
    
    return render(request, 'Juegos/ver_carrito.html', {'carrito': carrito, 'total': total})

def eliminar_del_carrito(request, producto_id):
    # Convertir el producto_id a cadena
    producto_id_str = str(producto_id)
    
    # Obtener el carrito de la sesión
    carrito = request.session.get('carrito', {})
    
    # Si el producto está en el carrito, eliminarlo
    if producto_id_str in carrito:
        del carrito[producto_id_str]
    
    # Actualizar el carrito en la sesión
    request.session['carrito'] = carrito
    
    return redirect('ver_carrito')

def vaciar_carrito(request):
    request.session['carrito'] = {}  # Vaciar el carrito en la sesión
    return redirect('ver_carrito')
