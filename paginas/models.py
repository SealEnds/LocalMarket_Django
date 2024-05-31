from django.db import models
from django_ckeditor_5.fields import CKEditor5Field

# python manage.py makemigrations -> crear migracion
# python manage.py sqlmigrate paginas 0001 -> generar sql
# pyhon manage.py migrate -> ejecutar sql

# Create your models here.
class Pagina(models.Model): # (models.Model) para heredar
    title = models.CharField(max_length=50, verbose_name='Título')
    content = CKEditor5Field(verbose_name='Descripción', config_name='extends')
    slug = models.CharField(unique=True, max_length=150,verbose_name='URL sencilla')
    order = models.IntegerField(default=0, verbose_name='Posición')
    visible = models.BooleanField(verbose_name='Visible')
    create_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha Creación")
    updated_at = models.DateTimeField(auto_now_add=True, verbose_name="Última actualización")
    class Meta:
        #nombres panel admin
        verbose_name = "Página"
        verbose_name_plural = "Páginas"
    def __str__(self):
        # mostrar título de página en panel de administración
        return self.title

