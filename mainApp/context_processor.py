from tiendas.models import Tag
from tiendas.models import Tienda

#context-processor para poder usar en cualquier parte, sin tener que llamar a la vista porque esta información estará en el Layout
def get_tags(request):
    # select con ORM de Django y filtrar por propiedad visible
    # filtrar los tags usados
    tagIdsInUse = Tienda.objects.filter(visible=True).values_list('tags', flat=True) # toma ids de tags usados en alguna tienda
    tags = Tag.objects.filter(id__in=tagIdsInUse).values_list('id', 'name') # filtra id en lista de ids
    return {
        'tags': tags,
        'ids': tagIdsInUse
    }