from django.db import models
from django.contrib.auth.models import User

class ChangeRole(models.Model):
    change_role_request = models.BooleanField(default=False, verbose_name='Petición Cambiar Rol')
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='change_role', verbose_name='User') # related_name permite a user acceder a ChangeRole desde registro de User: (user.change_role)
    class Meta:
        verbose_name = "Petición Vendedor"
        verbose_name_plural = "Peticiones Vendedores"

