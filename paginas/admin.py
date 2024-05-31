from django.contrib import admin
from .models import Pagina # importar modelos de carperta actual

class PaginaAdmin(admin.ModelAdmin): 
    readonly_fields = ('create_at', 'updated_at') # configurar campos solo lectura
    search_fields = ('title',) # añadir buscador # , aunque solo sea uno para que sea tupla
    list_filter = ('visible',) # filtrar por propiedad
    list_display = ('title', 'visible') # mostrar campos
    # ordenar
    ordering = ('-create_at',) # ordenar de más reciente a más antiguo

# Register your models here.
admin.site.register(Pagina, PaginaAdmin)

title = "TFC"
subtitle = "Administración"
admin.site.site_header = title
admin.site.site_title = title
admin.site.index_title = subtitle