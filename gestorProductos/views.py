from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect
from rest_framework.reverse import reverse
from .forms import ProductoForm, CategoriaForm
from .models import Producto, Categoria


def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))

    productos = Producto.objects.filter(usuario=request.user)

    return render(request, 'index.html', {'productos': productos})

@login_required
def crear_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            # Guardar el producto
            producto = form.save(commit=False)
            producto.usuario = request.user  # Asocia el producto al usuario logueado
            producto.save()  # Guarda el producto en la base de datos
            return redirect('listar_productos')  # Redirige a la lista de productos después de guardar
    else:
        form = ProductoForm()

    return render(request, 'crear_producto.html', {'form': form})
@login_required
def listar_productos(request):
    if request.user.is_superuser:
        productos = Producto.objects.all()  # Los superusuarios ven todos los productos
        print("Superusuario: Se muestran todos los productos.")  # Depuración
    else:
        productos = Producto.objects.filter(usuario=request.user)  # Los usuarios ven solo sus productos
        print(f"Usuario normal: Se muestran los productos de {request.user.username}.")  # Depuración

    return render(request, 'index.html', {'productos': productos})

def eliminar_producto(request, producto_id):
    # Obtén el producto por su ID
    producto = get_object_or_404(Producto, id=producto_id)

    if producto.usuario == request.user or request.user.is_superuser:
        producto.delete()  # Elimina el producto
        return redirect('listar_productos')  # Redirige a la lista de productos después de eliminar
    else:
        return redirect('listar_productos')



def editar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)

    if producto.usuario != request.user and not request.user.is_superuser:
        return redirect('index')

    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('listar_productos')
    else:
        form = ProductoForm(instance=producto)

    return render(request, 'crear_producto.html', {'form': form, 'producto': producto})


def listar_categorias(request):
    categorias = Categoria.objects.all()
    return render(request, 'lista_categorias.html', {'categorias': categorias})


def superuser_check(user):
    return user.is_superuser

@user_passes_test(superuser_check)
def agregar_categoria(request):
    if request.method == "POST":
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_categorias')
    else:
        form = CategoriaForm()

    return render(request, 'crear_categoria.html', {'form': form})


@user_passes_test(superuser_check)
def editar_categoria(request, categoria_id):
    categoria = Categoria.objects.get(id=categoria_id)
    if request.method == "POST":
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            return redirect('listar_categorias')
    else:
        form = CategoriaForm(instance=categoria)

    return render(request, 'crear_categoria.html', {'form': form})

@user_passes_test(superuser_check)
def eliminar_categoria(request, categoria_id):
    categoria = get_object_or_404(Categoria, id=categoria_id)
    if request.method == "POST":
            categoria.delete()
            return redirect('listar_categorias')
    else:
        return redirect('listar_categorias')
