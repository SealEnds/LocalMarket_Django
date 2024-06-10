from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from tiendas.models import Tag, Tienda, Producto, Review
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from .forms import TiendaForm, ProductoForm, ReviewForm
from django.contrib import messages
from django.utils.html import escape # filter html tags
import csv
from django.db import IntegrityError # check
import io # read files. StringIO, BytesIO: treat string and bytes as file like objects 

# Create your views here.
def getTiendas(request):

    tiendasPerPage = 6
    tiendas = Tienda.objects.all()
    pagination = Paginator(tiendas, tiendasPerPage)
    paginatorPage = request.GET.get('page') # tomar número página
    tiendasPorPagina = pagination.get_page(paginatorPage) # 

    return render(request, 'tiendas/tiendas.html', {
        'title': 'Tiendas',
        'tiendas': tiendasPorPagina
    })

def getTiendasByTag(request, tag_id):
    tag = Tag.objects.get(id=tag_id)
    tiendas = Tienda.objects.filter(tags=tag_id) # obtener tiendas que contengan tag_id en tags
    return render(request, 'tags/tag.html', {
        'tag': tag,
        'tiendas': tiendas
    })

def getTienda(request, tienda_id):
    # tienda = Tienda.objects.get(id=tienda_id)
    tienda = get_object_or_404(Tienda, id=tienda_id)

    productosPerPage = 9
    productos = Producto.objects.filter(tienda_id=tienda_id)
    pagination = Paginator(productos, productosPerPage)
    paginatorPage = request.GET.get('page') # tomar número página
    productosInPage = pagination.get_page(paginatorPage) # 
    is_tienda_owner = tienda.user_id == request.user.pk
    print(f"tienda: {productosInPage}")
    return render(request, 'tiendas/tienda.html', {
        'tienda': tienda,
        'productos': productosInPage,
        'is_owner': is_tienda_owner
    })

@login_required(login_url="login")
def createTienda(request):
    print('@@@ USER')
    is_owner = any(group.name == 'owner' for group in request.user.groups.all()) # comprobar si usuario está en grupo con permisos para crear tiendas
    if request.user.is_authenticated and is_owner:
        user_id = request.user.pk
        tienda = None
        if request.method == 'POST':
            tiendaForm = TiendaForm(request.POST, request.FILES)
            if tiendaForm.is_valid():
                tienda = tiendaForm.save(commit=False) # Don't save directly to change some values based on the form
                tienda.user_id = user_id  # Assign the current user to the tienda object
                tienda.save()  # Now save the tienda object to the database
                print(f'@@@ Tienda: {tienda.pk}')
                messages.success(request, 'Tienda creada con éxito')
                return HttpResponseRedirect(reverse('createtienda'))
        else:
            tiendaForm = TiendaForm()
        return render(request, 'tiendas/crearTienda.html', {
            'title': 'Crear Tienda',
            'tiendaForm': tiendaForm,
            'tienda': tienda
        })
    else:
        return redirect('login')

@login_required(login_url="login")
def editTienda(request, tienda_id): # usar template crearTienda cambiando el botón y añadiendo el valor del registro
    is_owner = any(group.name == 'owner' for group in request.user.groups.all())
    if request.user.is_authenticated and is_owner:
        tienda = get_object_or_404(Tienda, id=tienda_id)
        is_tienda_owner = tienda.user_id == request.user.pk
        if request.method == 'POST':
            tiendaForm = TiendaForm(request.POST, request.FILES, instance=tienda)
            if tiendaForm.is_valid():
                tiendaForm.save()
                messages.success(request, 'Tienda Actualizada')
                return HttpResponseRedirect(reverse('editTienda', args=[tienda_id]))
        else:
            tiendaForm = TiendaForm(instance=tienda) # pasar al formulario una instancia del modelo, no un id
        # tienda.content = escape(tienda.content)
        return render(request, 'tiendas/editarTienda.html', {
            'title': 'Editar Tienda',
            'tienda': tienda,
            'tiendaForm': tiendaForm,
            'is_owner': is_tienda_owner
        })
    else:
        return redirect('login')
    
@login_required(login_url="login")
def createProducto(request, tienda_id, producto_id=None): # reutilziar para editar si producto_id != None
    is_owner = any(group.name == 'owner' for group in request.user.groups.all())
    if request.user.is_authenticated and is_owner:
        user_id = request.user.pk
        tienda = get_object_or_404(Tienda, id=tienda_id, user_id=user_id)
        producto = None # para que no de error en la vista de crear
        action = 'create'
        productoForm = ProductoForm()

        if not producto_id: # opción crear producto
            if request.method == 'POST':
                productoForm = ProductoForm(request.POST, request.FILES)
                if productoForm.is_valid():
                    producto = productoForm.save(commit=False) # tomar resultados del formulario sin guardarlos
                    producto.tienda_id = tienda_id # como conseguir tienda id (param)
                    producto.user_id = user_id
                    producto.save()
                    messages.success(request, 'Producto creado con éxito')
                    # producto_url = reverse('editProducto', args=[tienda.pk, producto.pk])
                    # return HttpResponseRedirect(producto_url)
        else: # opción actualizar producto
            action = 'update'
            producto = get_object_or_404(Producto, id=producto_id, tienda_id=tienda_id, user_id=user_id)
            if request.method == 'POST':
                productoForm = ProductoForm(request.POST, request.FILES, instance=producto)
                print(f"Mostrar Mensajes: {producto.name}")
                print(f"Mostrar Mensajes: {producto.visible}")
                if productoForm.is_valid():
                    productoForm.save()
                    messages.success(request, 'Producto actualizado con éxito')
                    producto_url = reverse('producto', args=[producto.pk])
                    return HttpResponseRedirect(producto_url)
                else:
                    print(f"Mostrar Mensajes: {producto.name}")
                    print(f"Mostrar Mensajes: {producto.visible}")
                    productoForm = ProductoForm(instance=producto)
        return render(request, 'productos/crearProducto.html', {
            'title': 'Crear Producto' if action == 'create' else 'Editar Producto',
            'productoForm': productoForm,
            'producto': producto,
            'tienda': tienda,
            'action': action
        })
    else:
        return redirect('login')

def getProducto(request, producto_id):
    producto = Producto.objects.select_related('tienda').get(id=producto_id) # .get to get one. .filter to get many with condition .all() to get all. # select related tienda for editTienda url
    user_id = request.user.pk
    reviews = Review.objects.filter(producto_id=producto_id).select_related('user') # devuelve el objeto user relacionado con la review del usuario
    my_review = Review.objects.filter(producto_id=producto_id, user_id=user_id).select_related('user')
    if request.user.is_authenticated:
        if request.method == 'POST' and not my_review:
            reviewForm = ReviewForm(request.POST)
            if reviewForm.is_valid():
                review = reviewForm.save(commit=False) # no guardar todavía, hay que asignar un usuario y un producto
                review.user = request.user # id usuario
                review.producto_id = producto_id
                review.save()
                messages.success(request, 'Reseña creada con éxito')
                return HttpResponseRedirect(request.path_info) # evitar que se vuelva a crear otra review al recargar la pagina. request.path_info contiene la ruta URL sin parametros. Las variables del render siguen definidas.
        else:
            reviewForm = ReviewForm()
    # for message in messages.get_messages(request):
        # print(f"Mostrar Mensajes: {message}")
    return render(request, 'productos/producto.html', {
        'title': 'Detalle de Producto',
        'producto': producto,
        'reviews': reviews,
        'reviewForm': reviewForm,
        'myReview': my_review
    })

@login_required(login_url="login")
def deleteProducto(request, producto_id):
    is_owner = any(group.name == 'owner' for group in request.user.groups.all())
    if request.user.is_authenticated and is_owner:
        producto = Producto.objects.get(pk=producto_id)
        is_producto_owner = request.user.pk = producto.user_id
        if is_producto_owner and request.method == 'POST':
                producto.delete()
                messages.success(request, 'Reseña eliminada con éxito')
        tienda_url = reverse('tienda', args=[producto.tienda_id])
        return HttpResponseRedirect(tienda_url) # HttpResponseRedirect evita que se envíe el mismo formulario al recargar la página
    else: 
        return redirect('login')

@login_required(login_url="login")
def importCSV(request, tienda_id):
    is_owner = any(group.name == 'owner' for group in request.user.groups.all())
    if request.user.is_authenticated and is_owner:
        tienda = Tienda.objects.get(id=tienda_id)
        if tienda.user_id == request.user.pk: # comprobar que el usuario es el owner de la tienda
            # leer cada fila del csv y guardar el objeto
            if request.method == 'POST' and request.FILES.get('csv_file'):
                csv_file = request.FILES['csv_file']
                csv_data = csv_file.read().decode('utf-8') # solucionar error: iterator should return strings, not bytes 
                delimiter = ';' if ';' in csv_data.split('\n')[0] else ',' # delimiter en .csv puede ser ',' or ';'. Tomar primera linea y comprobar si se encuentra ';'
                reader = csv.DictReader(io.StringIO(csv_data),  delimiter=delimiter) # https://www.youtube.com/watch?v=t3BdM6JlAmY. DictReader() returns dictionary. reader() returns array.
                for row in reader:
                    row_ref = row.get('ref', 'default_value')
                    row_ref = row['ref']
                    productos_ref = Producto.objects.filter(ref=row_ref, tienda_id=tienda.pk)
                    if not productos_ref.exists(): # comprueba si existe o no un producto en la tienda con la referencia. Si no existe
                        new_producto = Producto(
                            name=row['name'],
                            description=row['description'],
                            price=row['price'],
                            visible=row['visible'].lower() == 'true', # condicional devuelve true si en cvs el valor es true case insensitive 
                            in_stock=row['in_stock'].lower() == 'true'
                        )
                        new_producto.tienda_id = tienda_id
                        new_producto.user_id = request.user.pk
                        new_producto.ref=row_ref
                        try:
                            new_producto.save()
                        except IntegrityError: # comprueba que no se repitan elementos únicos como ref
                            pass
                    else: # si existe, seleccionar el producto y actualizarlo
                        producto_ref = productos_ref.first() # primer elemento de la query
                        producto_ref.name = row['name']
                        producto_ref.content = row['description']
                        producto_ref.price = row['price']
                        producto_ref.visible = row['visible'].lower() == 'true'
                        producto_ref.in_stock = row['in_stock'].lower() == 'true'
                        producto_ref.save()
                # Example usage:
                # csv_file_path = 'path/to/your/csv/file.csv'
                # create_records_csv(csv_file_path)
                # return getTienda(request, tienda_id)
                tienda_url = reverse('tienda', kwargs={'tienda_id': tienda_id})
                return HttpResponseRedirect(tienda_url)
            else: 
                tienda_url = reverse('tienda', kwargs={'tienda_id': tienda_id})
                return HttpResponseRedirect(tienda_url)
        else:
            tienda_url = reverse('tienda', kwargs={'tienda_id': tienda_id})
            return HttpResponseRedirect(tienda_url)
    else:
        return redirect('login')
    
@login_required(login_url="login")
def deleteReview(request, review_id):
    review = Review.objects.select_related('producto').get(pk=review_id)
    producto_id = review.producto.pk
    if request.method == 'POST':
        review.delete()
        messages.success(request, 'Reseña eliminada con éxito')
    producto_url = reverse('producto', args=[producto_id])
    return HttpResponseRedirect(producto_url) # HttpResponseRedirect evita que se envíe el mismo formulario al recargar la página

@login_required(login_url="login")
def editReview(request, review_id):
    review = get_object_or_404(Review.objects.select_related('producto'), pk=review_id)
    tienda = get_object_or_404(Tienda, pk=review.producto.tienda_id)
    is_review_owner = review.user_id == request.user.pk

    if not is_review_owner:
        producto_url = reverse('producto', args=[review.producto.pk])
        return HttpResponseRedirect(producto_url)

    if request.method == 'POST' and 'edit_review_submit' in request.POST: # POST pero solo activado por el formulario de editar review
        reviewForm = ReviewForm(request.POST, instance=review)
        if reviewForm.is_valid():
            reviewForm.save()
            messages.success(request, 'Review Actualizada')
            producto_url = reverse('producto', args=[review.producto.pk])
            return HttpResponseRedirect(producto_url)
    else:
        reviewForm = ReviewForm(instance=review)

    return render(request, 'productos/editarReview.html', {
        'title': 'Editar Reseña',
        'tienda': tienda,
        'review': review,
        'reviewForm': reviewForm,
        'is_review_owner': is_review_owner
    })

def search(request):
    model = request.GET.get('model', 'tienda').strip()
    query = request.GET.get('query', 'all').strip()
    query = query.replace(' ', '') # asegurarse de que no se envíen espacios en blanco
    category = request.GET.get('category', 'all').strip()
    print(f"@@@@@@ AA: {model, query, category}")
    model_class = None
    if model == 'tienda':
        if query == 'all':
            return getTiendas(request)
        else:
            model_class = Tienda
    elif model == 'producto':
        model_class = Producto
    else:
        return getTiendas(request)
    print(f"@@@@@@ AA: {model_class}")
    if category != 'all':
        results = model_class.objects.filter(name__icontains=query, tags__name=category) # tags en plural
    else:
        results = model_class.objects.filter(name__icontains=query)
    print(f"@@@@@@ AA: {results}")
    resultsPerPage = 12
    pagination = Paginator(results, resultsPerPage)
    paginatorPage = request.GET.get('page')
    resultsInPage = pagination.get_page(paginatorPage) #
    print(f"@@@@@@ AA: {resultsInPage}")

    return render(request, 'search.html', {
        'title': 'Resultados Encontrados',
        'tiendas': resultsInPage,
        'productos': resultsInPage,
        'model': model,
        'query': query,
        'category': category
    })
