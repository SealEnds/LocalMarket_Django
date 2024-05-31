from typing import Any
from django.contrib import admin
from .models import ChangeRole
from django.contrib.auth.models import User

class ChangeRoleAdmin(admin.ModelAdmin):
    readonly_fields = ('user',)
    search_fields = ('change_role_request',)
    list_display = ('user', 'change_role_request')
    list_filter = ('change_role_request',)

# Register your models here.
admin.site.register(ChangeRole, ChangeRoleAdmin)

