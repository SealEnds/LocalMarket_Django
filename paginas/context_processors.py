from paginas.models import Pagina

def get_paginas(request):
    # select con ORM de Django y filtrar por propiedad visible
    paginas = Pagina.objects.filter(visible=True).order_by('order').values_list('id', 'title', 'slug')
    return {
        'paginas': paginas
    }