from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.getTiendas, name="index"),
    path('tiendas/', views.getTiendas, name="tiendas"),
    path('tag/<int:tag_id>', views.getTiendasByTag, name="tag"),
    path('crear-tienda', views.createTienda, name="createtienda"),
    path('tienda/<int:tienda_id>', views.getTienda, name="tienda"),
    path('editar-tienda/<int:tienda_id>', views.editTienda, name="editTienda"),
    path('crear-producto/<int:tienda_id>', views.createProducto, name="createProducto"),
    path('crear-producto/<int:tienda_id>/<int:producto_id>/', views.createProducto, name="editProducto"), # 2 parametro producto_id para editar el productos
    path('producto/<int:producto_id>', views.getProducto, name="producto"),
    path('borrar-producto/<int:producto_id>', views.deleteProducto, name="deleteProducto"),
    path('importar-productos/<int:tienda_id>', views.importCSV, name="importCSV"),
    path('borrar-review/<int:review_id>', views.deleteReview, name="deleteReview"),
    path('editar-review/<int:review_id>', views.editReview, name="editReview"),
    path('buscar', views.search, name="search")
]

if settings.DEBUG: #add this
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)