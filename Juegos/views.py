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
        form = ProductoForm(request.POST, request.FILES)  # Asegúrate de incluir request.FILES
        if form.is_valid():
            form.save()
            return redirect('listar_productos')  # Redirige tras guardar el producto
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
    

from django.shortcuts import render, redirect
from .models import Perfil  # Asegúrate de que has importado el modelo Perfil
from .forms import PerfilForm  # Asegúrate de que has importado el formulario

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render
from .models import Perfil  # Asegúrate de que este sea el modelo de perfil que has creado

from .forms import PerfilForm

@login_required
def perfil_usuario(request):
    perfil = Perfil.objects.get(user=request.user)

    if request.method == 'POST':
        form = PerfilForm(request.POST, request.FILES, instance=perfil)
        if form.is_valid():
            form.save()
            return redirect('perfil_usuario')  # Redirigir a la página de perfil después de guardar
    else:
        form = PerfilForm(instance=perfil)

    if request.user.is_superuser:
        usuarios = User.objects.all()
    else:
        usuarios = None

    context = {
        'user': request.user,
        'perfil': perfil,
        'form': form,
        'usuarios': usuarios,
    }
    return render(request, 'Juegos/perfil.html', context)


from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Perfil.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.perfil.save()

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
    # Obtener el carrito de la sesión
    carrito = request.session.get('carrito', {})

    # Calcular el total de cada producto (precio * cantidad) y el total general
    total = 0
    for producto_id, item in carrito.items():
        item['total'] = item['precio'] * item['cantidad']  # Añadimos el total por producto
        total += item['total']  # Sumamos al total general

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

from django.shortcuts import redirect

def actualizar_cantidad_carrito(request, producto_id):
    if request.method == 'POST':
        nueva_cantidad = int(request.POST.get('cantidad', 1))
        carrito = request.session.get('carrito', {})
        
        producto_id_str = str(producto_id)
        
        if producto_id_str in carrito:
            if nueva_cantidad > 0:
                carrito[producto_id_str]['cantidad'] = nueva_cantidad
            else:
                del carrito[producto_id_str]  # Eliminar el producto si la cantidad es 0

        request.session['carrito'] = carrito
    
    return redirect('ver_carrito')

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Producto
from .serializers import ProductoSerializer

@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])  # Requiere que el usuario esté autenticado para acceder a la API
def productos_api(request, pk=None):
    # GET - Listar productos o obtener uno en específico
    if request.method == 'GET':
        if pk:
            producto = get_object_or_404(Producto, pk=pk)
            serializer = ProductoSerializer(producto)
        else:
            productos = Producto.objects.all()
            serializer = ProductoSerializer(productos, many=True)
        return Response(serializer.data)
    
    # POST - Crear un nuevo producto
    elif request.method == 'POST':
        serializer = ProductoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # PUT - Actualizar un producto existente
    elif request.method == 'PUT':
        producto = get_object_or_404(Producto, pk=pk)
        serializer = ProductoSerializer(producto, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # DELETE - Eliminar un producto
    elif request.method == 'DELETE':
        producto = get_object_or_404(Producto, pk=pk)
        producto.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Producto, Pedido
from .serializers import ProductoSerializer, PedidoSerializer

# ViewSet para el modelo Producto
class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()  # Recuperar todos los productos de la base de datos
    serializer_class = ProductoSerializer  # Usar el serializador definido para Producto
    permission_classes = [IsAuthenticated]  # Requiere que el usuario esté autenticado para acceder

# ViewSet para el modelo Pedido
class PedidoViewSet(viewsets.ModelViewSet):
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer
    permission_classes = [IsAuthenticated]  # Solo usuarios autenticados pueden acceder a este ViewSet

    # Sobrescribimos el método 'perform_create' para asignar el usuario logueado
    def perform_create(self, serializer):
        # Asignamos el usuario autenticado al pedido
        serializer.save(usuario=self.request.user)

from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Pedido, Producto
from .forms import PedidoForm

from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Pedido, Producto
from .forms import PedidoForm

# Vista para listar los pedidos
class ListaPedidosView(LoginRequiredMixin, ListView):
    model = Pedido
    template_name = 'Juegos/lista_pedidos.html'
    context_object_name = 'pedidos'
    login_url = 'login'  # Redirecciona a la página de login si no está autenticado

# Vista para crear un nuevo pedido
class CrearPedidoView(LoginRequiredMixin, CreateView):
    model = Pedido
    form_class = PedidoForm
    template_name = 'Juegos/crear_pedido.html'
    success_url = reverse_lazy('lista_pedidos')
    login_url = 'login'  # Redirigir si no está autenticado

    def form_valid(self, form):
        # Asignar el usuario autenticado al campo usuario
        form.instance.usuario = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['productos'] = Producto.objects.all()  # Pasar productos al contexto
        return context

# Vista para editar un pedido existente
class EditarPedidoView(LoginRequiredMixin, UpdateView):
    model = Pedido
    form_class = PedidoForm
    template_name = 'Juegos/editar_pedido.html'
    success_url = reverse_lazy('lista_pedidos')
    login_url = 'login'

# Vista para eliminar un pedido existente
class EliminarPedidoView(LoginRequiredMixin, DeleteView):
    model = Pedido
    template_name = 'Juegos/confirmar_eliminar_pedido.html'
    success_url = reverse_lazy('lista_pedidos')
    login_url = 'login'

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render
from django.core.cache import cache
import requests
from deep_translator import GoogleTranslator  # Importar el traductor

    
@login_required
def noticias(request):
    url = "https://www.mmobomb.com/api1/latestnews"
    cache_key = 'news_data'
    cache_timeout = 3600  # 1 hora en segundos

    # Intentamos obtener los datos desde la caché
    news_data = cache.get(cache_key)

    if not news_data:
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
            }
            response = requests.get(url, headers=headers, timeout=10)  # Agregamos los headers a la solicitud
            response.raise_for_status()
            news_data = response.json()
            cache.set(cache_key, news_data, cache_timeout)
        except requests.exceptions.RequestException as e:
            print(f"Error fetching news: {e}")
            news_data = []

    # Filtramos y traducimos los datos
    filtered_news = []
    for item in news_data:
        if all(k in item for k in ('title', 'short_description', 'thumbnail', 'article_url')):
            # Traducción
            try:
                translated_title = GoogleTranslator(source='auto', target='es').translate(item['title'])
                translated_description = GoogleTranslator(source='auto', target='es').translate(item['short_description'])
            except Exception as e:
                print(f"Error translating: {e}")
                translated_title = item['title']
                translated_description = item['short_description']

            filtered_news.append({
                'title': translated_title,
                'short_description': translated_description,
                'thumbnail': item['thumbnail'],
                'article_url': item['article_url']
            })

    # Procesar la búsqueda
    query = request.GET.get('query', '')
    if query:
        filtered_news = [item for item in filtered_news if query.lower() in item['title'].lower() or query.lower() in item['short_description'].lower()]

    # Paginamos las noticias, 5 por página
    paginator = Paginator(filtered_news, 5)
    page = request.GET.get('page')

    try:
        paginated_news = paginator.page(page)
    except PageNotAnInteger:
        paginated_news = paginator.page(1)
    except EmptyPage:
        paginated_news = paginator.page(paginator.num_pages)

    return render(request, 'Juegos/noticias.html', {'news': paginated_news, 'query': query})


from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render
import requests

@login_required  # Solo usuarios autenticados podrán acceder
def get_free_games(request):
    url = "https://www.freetogame.com/api/games"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        free_games = []
        
        # Procesar los juegos gratuitos
        for game in data:
            free_games.append({
                'title': game.get('title'),
                'description': game.get('short_description'),
                'image': game.get('thumbnail'),
                'url': game.get('game_url'),
                'platform': game.get('platform'),
                'genre': game.get('genre'),
                'release_date': game.get('release_date'),  # Asumiendo que este campo está disponible
            })

        # Filtrado
        genre_filter = request.GET.get('genre')

        order_by = request.GET.get('order_by', 'title')  # Ordenar por título por defecto
        order_direction = request.GET.get('order_direction', 'asc')  # Orden ascendente por defecto

        if genre_filter:
            free_games = [game for game in free_games if game['genre'] == genre_filter]

        # Ordenar
        reverse = order_direction == 'desc'
        if order_by == 'release_date':
            free_games.sort(key=lambda x: x['release_date'], reverse=reverse)  # Ordenar por fecha
        elif order_by == 'genre':
            free_games.sort(key=lambda x: x['genre'], reverse=reverse)  # Ordenar por género
        else:  # Por defecto, ordenar por título
            free_games.sort(key=lambda x: x['title'], reverse=reverse)

        # Paginación
        paginator = Paginator(free_games, 10)  # Mostrar 10 juegos por página
        page_number = request.GET.get('page')  # Obtener el número de página de la solicitud
        page_obj = paginator.get_page(page_number)  # Obtener la página actual

        # Renderizar los juegos en la plantilla
        return render(request, 'Juegos/free_games.html', {
            'page_obj': page_obj,
            'genres': set(game['genre'] for game in data),
            'platforms': set(game['platform'] for game in data),
            'order_direction': order_direction,
        })

    except requests.exceptions.RequestException as e:
        return render(request, 'Juegos/free_games.html', {'error': str(e)})
    except Exception as e:
        return render(request, 'Juegos/free_games.html', {'error': str(e)})
