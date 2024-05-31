from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse
from tiendas.models import Tienda, Review
from mainApp.models import ChangeRole
from django.contrib.auth.models import User
from .forms import RegisterForm
from .forms import UpdateUserForm
from django.contrib import messages # mensajes flash
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

def index(request):
    return render(request, 'mainApp/index.html', {'title': 'Inicio'})

def nosotros(request):
    return render(request, 'mainApp/nosotros.html', {'title': 'Sobre Nosotros'})

def registerView(request):
    if request.user.is_authenticated: # redigir si ya se ha iniciado sesión
        return redirect('index')
    else:
        registerForm = RegisterForm() # usar formulario personalizado
        if request.method == 'POST': # si se envía el formulario
            registerForm = RegisterForm(request.POST) # recibir valores del formulario
            if registerForm.is_valid():
                registerForm.save()
                messages.success(request, 'Has creado un Usuario con éxito')
                registro_url = reverse('registro')
                return HttpResponseRedirect(registro_url)
        return render(request, 'mainApp/register.html', {
            'title': 'Registro',
            'registerForm': registerForm    
    })

def loginView(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        if request.method == 'POST':
            usersname = request.POST.get('username')
            userspass = request.POST.get('password')
            user = authenticate(request, username=usersname, password=userspass)
            if user is not None:
                login(request, user)
                login_url = reverse('login')
                return HttpResponseRedirect(login_url)
            else:
                messages.warning(request, 'Error al Identificarse')

        return render(request, 'mainApp/login.html', {
            'title': 'Login'
        })

def logoutView(request):
    logout(request)
    return redirect('login')

@login_required(login_url="login")
def perfil(request):
    if request.user.is_authenticated:
        is_owner = any(group.name == 'owner' for group in request.user.groups.all())
        # actualizar perfil __________________________________________________________________
        if request.method == 'POST':
            registerForm = UpdateUserForm(request.POST, instance=request.user)
            if registerForm.is_valid():
                registerForm.save()
                messages.success(request, 'Usuario Actualizado') 
        else:
            registerForm = UpdateUserForm(instance=request.user)
        # mis tiendas ________________________________________________________________________
        userId = request.user.pk 
        tiendas = Tienda.objects.filter(user_id=userId)
        # mis reseñas ________________________________________________________________________
        reviews = Review.objects.filter(user_id=userId).select_related('producto').order_by('-updated_at')
        # comprobar si se ha pedido ser vendedor
        try:
            change_role_instance = ChangeRole.objects.get(user=request.user)
            change_role_request = change_role_instance.change_role_request               
        except ChangeRole.DoesNotExist:
            change_role_request = False
        return render(request, 'mainApp/perfil.html', {
            'title': 'Perfil',
            'tiendas': tiendas,
            'registerForm': registerForm,
            'reviews': reviews,
            'is_owner': is_owner,
            'change_role_request': change_role_request
        })
    else:
        return redirect('login')
    
@login_required(login_url="login")
def changeRole(request, user_id):
    if request.user.is_authenticated:
        user = get_object_or_404(User, pk=user_id)
        change_role, created = ChangeRole.objects.get_or_create(user=user) # crear o editar el que ya existe. Solo puede haber uno por usuario
        change_role.change_role_request = True        
        change_role.save()
        return redirect('perfil')