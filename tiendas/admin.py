from typing import Any
from django.contrib import admin
from .models import Tag, Tienda, Producto, Review
from django.contrib.auth.models import User

# mostrar en admin los campos de solo lectura
class TiendaAdmin(admin.ModelAdmin): 
    readonly_fields = ('user', 'created_at', 'updated_at')
    search_fields = ('name','user__username','tags__name')
    list_display = ('name', 'user', 'visible')
    list_filter = ('visible', 'user__username')
    def save_model(self, request: Any, obj: Any, form: Any, change: Any) -> None: # -> None es como void
        if not obj.user_id:
            obj.user_id = request.user.pk
        obj.save()
        # return super().save_model(request, obj, form, change)
class TagAdmin(admin.ModelAdmin):
    search_fields = ('name',)
class ProductoAdmin(admin.ModelAdmin):
    readonly_fields = ('user', 'tienda', 'created_at', 'updated_at')
    search_fields = ('name','visible')
    list_display = ('name', 'user', 'tienda', 'visible')
    list_filter = ('visible', 'tienda__name')
class ProductoAdmin(admin.ModelAdmin):
    readonly_fields = ('user', 'tienda', 'created_at', 'updated_at')
    search_fields = ('name','visible')
    list_display = ('name', 'user', 'tienda', 'visible')
    list_filter = ('visible', 'tienda__name')
# class DiscountAdmin(admin.ModelAdmin):
#     search_fields = ('name', 'percentage')
#     list_display = ('name', 'percentage')
#     list_filter = ('percentage',)
# class UserProductDiscountAdmin(admin.ModelAdmin):
#     readonly_fields = ('user', 'product', 'discount')
#     search_fields = ('detail', 'user', 'product', 'discount')
#     list_display = ('detail','user', 'product', 'discount')
class ReviewAdmin(admin.ModelAdmin):
    readonly_fields = ('user', 'producto', 'created_at', 'updated_at')
    search_fields = ('rating', 'visible')
    list_display = ('review_content','rating', 'visible')
    list_filter = ('rating', 'visible')

# Register your models here.
admin.site.register(Tienda, TiendaAdmin)
admin.site.register(Producto, ProductoAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Review, ReviewAdmin)
# admin.site.register(Role, RoleAdmin)
# admin.site.register(UserRole, UserRoleAdmin)
# admin.site.register(Discount, DiscountAdmin)
# admin.site.register(UserProductDiscount, UserProductDiscountAdmin)

title = "TFC"
subtitle = "Administración"
admin.site.site_header = title
admin.site.site_title = title
admin.site.index_title = subtitle