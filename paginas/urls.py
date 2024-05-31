from django.urls import path
from . import views

urlpatterns = [
    path('pagina/<str:urlname>', views.pagina, name="pagina")
]
