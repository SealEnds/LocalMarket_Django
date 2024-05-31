"""
URL configuration for TFC project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from mainApp import views # importar vistas para usar en rutas
#import paginas.views # importar de modo para que no haya conflicto entre el nombre views de cada app

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', views.index, name="index"),
    path('inicio/', views.index, name="index"),
    # path('nosotros/', views.nosotros, name="nosotros"),
    path('registro/', views.registerView, name="registro"),
    path('login/', views.loginView, name="login"),
    path('logout/', views.logoutView, name="logout"),
    path('perfil/', views.perfil, name="perfil"),
    path('cambiar-rol/<int:user_id>', views.changeRole, name="changeRole"),
    # path('pagina/<str:urlname>', paginas.views.pagina, name="pagina") # movido a urls.py de paginas
    path('', include('paginas.urls')), # llamar urls.py de paginas
    path('', include('tiendas.urls')),
    # ckeditor
    path('ckeditor5/', include('django_ckeditor_5.urls')),
]

# media path
if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)