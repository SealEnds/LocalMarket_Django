from django.shortcuts import render
from .models import Pagina

# Create your views here.
def pagina(request, urlname):
    # get pagina where slug = parametro pasado por url. urls.py pagina/<str:urlname>
    pagina = Pagina.objects.get(slug=urlname)
    return render(request, "paginas/pagina.html", {
        "pagina": pagina
    })